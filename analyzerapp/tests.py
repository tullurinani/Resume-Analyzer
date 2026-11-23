from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.test import TestCase, SimpleTestCase
from django.urls import reverse

from .ai.question_generator import generate_questions
from .ai.resume_parser import parse_resume_text
from .ai.scoring_model import calculate_score
from .forms import CandidateForm
from .models import Candidate


class ResumeParsingTests(SimpleTestCase):
    def test_extracts_known_skills_and_education(self):
        parsed = parse_resume_text("B.Tech in Data Science. Built a Python and Django app with SQL and REST API integration.")
        self.assertIn("Python", parsed["skills"])
        self.assertIn("Django", parsed["skills"])
        self.assertTrue(parsed["education"])

    def test_question_generation_uses_resume_signals(self):
        questions = generate_questions({"skills": ["Java", "SQL"], "education": [], "experience": []})
        self.assertTrue(any("Java" in question or "object-oriented" in question for question in questions))
        self.assertTrue(any("SQL" in question for question in questions))


class ScoreTests(SimpleTestCase):
    def test_calculates_average(self):
        self.assertEqual(calculate_score(80, 70, 90), 80.0)

    def test_rejects_scores_outside_range(self):
        with self.assertRaises(ValueError):
            calculate_score(120, 70, 90)

    def test_rejects_non_integer_scores(self):
        with self.assertRaises(TypeError):
            calculate_score(80.5, 70, 90)


class CandidateAccountTests(TestCase):
    def test_registration_stores_hashed_password(self):
        form = CandidateForm(data={
            "name": "Test Candidate",
            "email": "candidate@example.com",
            "phone": "9000000000",
            "address": "Hyderabad",
            "state": "Telangana",
            "password": "A-strong-test-password-123",
            "confirm_password": "A-strong-test-password-123",
        })
        self.assertTrue(form.is_valid(), form.errors)
        candidate = form.save()
        self.assertNotEqual(candidate.password, "A-strong-test-password-123")
        self.assertTrue(check_password("A-strong-test-password-123", candidate.password))

    def test_candidate_login_sets_session(self):
        candidate = Candidate.objects.create(
            name="Test Candidate", email="login@example.com", phone="9000000000",
            address="Hyderabad", state="Telangana",
            password=make_password("Candidate-password-123"),
        )
        response = self.client.post(reverse("user_login"), {
            "email": "login@example.com", "password": "Candidate-password-123",
        })
        self.assertRedirects(response, reverse("user_dashboard"))
        self.assertEqual(self.client.session.get("candidate_id"), candidate.pk)

    def test_staff_dashboard_requires_staff_login(self):
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)
        User = get_user_model()
        staff = User.objects.create_user(username="reviewer", password="Strong-staff-password-123", is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_status_update_rejects_get_and_updates_only_for_staff(self):
        candidate = Candidate.objects.create(
            name="Test Candidate", email="status@example.com", phone="9000000000",
            address="Hyderabad", state="Telangana",
            password=make_password("Candidate-password-123"),
        )
        response = self.client.post(reverse("update_status", args=[candidate.pk]), {"status": "Accepted"})
        self.assertEqual(response.status_code, 302)
        candidate.refresh_from_db()
        self.assertEqual(candidate.status, "Pending")
        staff = get_user_model().objects.create_user(
            username="reviewer2", password="Strong-staff-password-123", is_staff=True
        )
        self.client.force_login(staff)
        response = self.client.post(reverse("update_status", args=[candidate.pk]), {"status": "Accepted"})
        self.assertRedirects(response, reverse("admin_dashboard"))
        candidate.refresh_from_db()
        self.assertEqual(candidate.status, "Accepted")
