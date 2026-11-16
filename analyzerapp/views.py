# analyzerapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import Resume, Interview
from .forms import ResumeUploadForm
from .ai.resume_parser import parse_resume
from .ai.question_generator import generate_questions
from .ai.scoring_model import calculate_score
from django.contrib.sessions.backends.db import SessionStore
  
# ---------- INDEX ----------
def index(request):
    return render(request, 'index.html')

# ---------- USER ----------
def user_register(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if Candidate.objects.filter(email=email).exists():
                return render(request, 'register.html', {'form': form, 'error': 'Email already exists.'})
            
            form.save()
            return redirect('user_login')  # ✅ redirect to login page
    else:
        form = CandidateForm()
    return render(request, 'register.html', {'form': form})


from .forms import LoginForm

def user_login(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                candidate = Candidate.objects.get(email=email, password=password)
                request.session['candidate_id'] = candidate.id
                return redirect('user_dashboard')  # ✅ make sure this URL exists
            except Candidate.DoesNotExist:
                error = "Invalid email or password."
    else:
        form = LoginForm()

    return render(request, 'user_login.html', {'form': form, 'error': error})


def user_dashboard(request):
    candidate_id = request.session.get('candidate_id')
    if candidate_id:
        candidate = Candidate.objects.get(id=candidate_id)
        return render(request, 'user_dashboard.html', {'candidate': candidate})
    return redirect('user_login')




from django.core.files.storage import FileSystemStorage

def upload_resume(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('user_login')

    candidate = Candidate.objects.get(id=candidate_id)

    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']

        # Save to media/resumes/uploaded/
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'resumes/uploaded'))
        filename = fs.save(resume_file.name, resume_file)
        file_path = os.path.join('resumes/uploaded', filename)

        # Save to Resume model
        Resume.objects.update_or_create(
            candidate=candidate,
            defaults={'resume_file': file_path}
        )

        # Save absolute path to session for AI parsing
        absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
        request.session['uploaded_resume_path'] = absolute_path

        return redirect('user_dashboard')

    return render(request, 'resume_upload.html')


from django.conf import settings
import os

# def resume_upload(request):
#     if request.method == 'POST' and request.FILES.get('resume'):
#         resume = request.FILES['resume']

#         # Save file to resumes/uploaded/
#         upload_dir = os.path.join(settings.BASE_DIR, 'resumes', 'uploaded')
#         os.makedirs(upload_dir, exist_ok=True)

#         fs = FileSystemStorage(location=upload_dir)
#         filename = fs.save(resume.name, resume)
#         full_path = os.path.join(upload_dir, filename)

#         # ✅ Save full path in session
#         request.session['uploaded_resume_path'] = full_path

#         return redirect('user_dashboard')
#     return render(request, 'resume_upload.html')
from .models import Candidate
from .forms import CandidateForm
def resume_upload(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            request.session['candidate_id'] = candidate.id
            request.session['uploaded_resume_path'] = candidate.resume_file.path
            return redirect('user_dashboard')
    else:
        form = CandidateForm()
    return render(request, 'resume_upload.html', {'form': form})

from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import HttpResponse

@csrf_exempt
def upload_video(request):
    candidate_id = request.session.get('candidate_id')
    if candidate_id and request.method == 'POST':
        candidate = Candidate.objects.get(id=candidate_id)
        video_data = request.FILES['video']
        candidate.interview_video.save(f"interview_{candidate_id}.webm", video_data)
        candidate.save()
        return HttpResponse("Uploaded")
    return HttpResponse("Failed", status=400)

# analyzerapp/views.py
from django.shortcuts import render
from .ai.resume_parser import parse_resume
from .ai.question_generator import generate_questions

def start_interview(request):
    resume_path = request.session.get('uploaded_resume_path')
    if resume_path and os.path.exists(resume_path):
        parsed = parse_resume(resume_path)
        questions = generate_questions(parsed)
        questions_list = questions.split('\n')
    else:
        questions_list = ["❗ Please upload your resume first."]
    
    return render(request, 'interview.html', {'questions': questions_list})



def upload_interview_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        interview = Interview.objects.get(user=request.user)
        video = request.FILES['video']
        interview.video_file.save(f"{request.user.username}_interview.webm", ContentFile(video.read()))
        interview.save()
        return redirect('user_dashboard')
    return render(request, 'interview.html', {'error': 'No video received'})

# ---------- ADMIN ----------
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, "❌ Invalid credentials.")
            return redirect('admin_login')
    return render(request, 'admin_login.html')  

def admin_dashboard(request):
    candidates = Candidate.objects.all().order_by('-submitted_at')
    return render(request, 'admin_dashboard.html', {'candidates': candidates})


from django.views.decorators.csrf import csrf_protect
from random import randint

@csrf_protect
def update_status(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        candidate.status = new_status

        # ✅ Score update logic
        if new_status == "Rejected":
            candidate.score = randint(10, 34)
        elif new_status == "Accepted":
            candidate.score = randint(75, 100)
        elif new_status == "Pending":
            candidate.score = None
        candidate.save()

        # ✅ Send email after saving
        send_status_email(candidate.email, candidate.name, new_status)

    return redirect('admin_dashboard')

def score_interview(request, id):
    interview = get_object_or_404(Interview, id=id)
    if request.method == 'POST':
        comm = int(request.POST.get('comm_score'))
        rel = int(request.POST.get('rel_score'))
        conf = int(request.POST.get('conf_score'))
        total = calculate_score(comm, rel, conf)
        interview.communication_score = comm
        interview.relevance_score = rel
        interview.confidence_score = conf
        interview.total_score = total
        interview.save()
        return redirect('admin_dashboard')
    return render(request, 'score_result.html', {'interview': interview})

def accept_interview(request, id):
    interview = get_object_or_404(Interview, id=id)
    interview.status = 'Accepted'
    interview.save()
    return redirect('admin_dashboard')

def reject_interview(request, id):
    interview = get_object_or_404(Interview, id=id)
    interview.status = 'Rejected'
    interview.save()
    return redirect('admin_dashboard')

def admin_logout(request):
    request.session.flush()
    return redirect('index')


from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return redirect('index')  