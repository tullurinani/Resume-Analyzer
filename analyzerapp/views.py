"""Views for resume upload, practice interviews and staff review."""
from __future__ import annotations

import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .ai.question_generator import generate_questions
from .ai.resume_parser import parse_resume
from .ai.scoring_model import calculate_score
from .forms import CandidateForm, LoginForm, ResumeUploadForm
from .models import Candidate, Interview


def index(request):
    return render(request, "index.html")


def user_register(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            if Candidate.objects.filter(email__iexact=form.cleaned_data["email"]).exists():
                form.add_error("email", "An account with this email already exists.")
            else:
                form.save()
                messages.success(request, "Your account was created. You can sign in now.")
                return redirect("user_login")
    else:
        form = CandidateForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip()
        password = form.cleaned_data["password"]
        candidate = Candidate.objects.filter(email__iexact=email).first()
        if candidate and check_password(password, candidate.password):
            request.session.flush()
            request.session["candidate_id"] = candidate.pk
            messages.success(request, f"Welcome back, {candidate.name}.")
            return redirect("user_dashboard")

        # One-time migration path: old local accounts stored plaintext passwords.
        # A legacy password is immediately re-hashed after a successful login.
        if candidate and candidate.password and candidate.password == password:
            candidate.password = make_password(password)
            candidate.save(update_fields=["password"])
            request.session.flush()
            request.session["candidate_id"] = candidate.pk
            messages.success(request, f"Welcome back, {candidate.name}. Your password was secured.")
            return redirect("user_dashboard")

        messages.error(request, "The email or password is incorrect.")
    return render(request, "user_login.html", {"form": form})


def _current_candidate(request):
    candidate_id = request.session.get("candidate_id")
    if not candidate_id:
        return None
    return Candidate.objects.filter(pk=candidate_id).first()


def user_dashboard(request):
    candidate = _current_candidate(request)
    if candidate is None:
        return redirect("user_login")
    latest_resume = candidate.resumes.order_by("-uploaded_at").first()
    return render(request, "user_dashboard.html", {"candidate": candidate, "latest_resume": latest_resume})


def upload_resume(request):
    candidate = _current_candidate(request)
    if candidate is None:
        return redirect("user_login")

    form = ResumeUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        resume = form.save(commit=False)
        resume.candidate = candidate
        resume.save()
        request.session["uploaded_resume_path"] = resume.resume_file.path
        messages.success(request, "Resume uploaded successfully.")
        return redirect("user_dashboard")

    return render(request, "resume_upload.html", {"form": form})


def start_interview(request):
    candidate = _current_candidate(request)
    if candidate is None:
        return redirect("user_login")

    latest_resume = candidate.resumes.order_by("-uploaded_at").first()
    questions = []
    if latest_resume and latest_resume.resume_file and os.path.isfile(latest_resume.resume_file.path):
        try:
            parsed = parse_resume(latest_resume.resume_file.path)
            questions = generate_questions(parsed)
        except Exception as exc:
            messages.error(request, f"The resume could not be parsed: {exc}")
    else:
        messages.info(request, "Upload a PDF or DOCX resume before starting an interview.")

    return render(request, "interview.html", {"candidate": candidate, "questions": questions})


@require_POST
def upload_video(request):
    candidate = _current_candidate(request)
    if candidate is None:
        return JsonResponse({"ok": False, "error": "Please sign in again."}, status=401)

    video = request.FILES.get("video")
    if video is None:
        return JsonResponse({"ok": False, "error": "No video file was received."}, status=400)
    if video.size > 100 * 1024 * 1024:
        return JsonResponse({"ok": False, "error": "The recording is larger than 100 MB."}, status=413)
    extension = os.path.splitext(video.name)[1].lower()
    if extension not in {".webm", ".mp4", ".mov"}:
        return JsonResponse({"ok": False, "error": "Unsupported video format."}, status=400)

    candidate.interview_video.save(f"candidate_{candidate.pk}{extension}", video, save=True)
    return JsonResponse({"ok": True, "message": "Interview recording saved."})


def _staff_check(user):
    return user.is_authenticated and user.is_active and (user.is_staff or user.is_superuser)


staff_required = user_passes_test(_staff_check, login_url="admin_login")


def admin_login(request):
    if request.user.is_authenticated and _staff_check(request.user):
        return redirect("admin_dashboard")
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and _staff_check(user):
            login(request, user)
            return redirect("admin_dashboard")
        error = "Sign-in failed. Use an active Django staff account."
    return render(request, "admin_login.html", {"error": error})


@staff_required
def admin_dashboard(request):
    candidates = Candidate.objects.all().order_by("-submitted_at")
    return render(request, "admin_dashboard.html", {"candidates": candidates})


@staff_required
@require_POST
def update_status(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    new_status = request.POST.get("status", "").strip()
    if new_status not in {"Pending", "Accepted", "Rejected"}:
        messages.error(request, "Invalid candidate status.")
        return redirect("admin_dashboard")

    candidate.status = new_status
    candidate.save(update_fields=["status"])

    if settings.EMAIL_HOST or settings.EMAIL_BACKEND.endswith("console.EmailBackend"):
        try:
            send_mail(
                subject="Application status update",
                message=f"Hello {candidate.name}, your application status is now: {new_status}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[candidate.email],
                fail_silently=True,
            )
        except Exception:
            pass

    messages.success(request, f"Updated {candidate.name}'s status to {new_status}.")
    return redirect("admin_dashboard")


@staff_required
def score_interview(request, id):
    interview = get_object_or_404(Interview, pk=id)
    if request.method == "POST":
        try:
            communication = int(request.POST.get("comm_score", ""))
            relevance = int(request.POST.get("rel_score", ""))
            confidence = int(request.POST.get("conf_score", ""))
            total = calculate_score(communication, relevance, confidence)
        except (TypeError, ValueError) as exc:
            messages.error(request, str(exc))
            return redirect("admin_dashboard")

        interview.communication_score = communication
        interview.relevance_score = relevance
        interview.confidence_score = confidence
        interview.total_score = total
        interview.save(update_fields=["communication_score", "relevance_score", "confidence_score", "total_score"])
        messages.success(request, "Interview score saved.")
        return redirect("admin_dashboard")
    return render(request, "score_result.html", {"interview": interview})


@staff_required
@require_POST
def accept_interview(request, id):
    interview = get_object_or_404(Interview, pk=id)
    interview.status = "Accepted"
    interview.save(update_fields=["status"])
    return redirect("admin_dashboard")


@staff_required
@require_POST
def reject_interview(request, id):
    interview = get_object_or_404(Interview, pk=id)
    interview.status = "Rejected"
    interview.save(update_fields=["status"])
    return redirect("admin_dashboard")


def admin_logout(request):
    logout(request)
    return redirect("index")


def user_logout(request):
    request.session.flush()
    return redirect("index")
