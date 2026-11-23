from django import forms
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator

from .models import Candidate, Resume


class CandidateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), min_length=8)

    class Meta:
        model = Candidate
        fields = ["name", "email", "phone", "address", "state"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "state": forms.TextInput(attrs={"placeholder": "State / region"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["state"].required = False
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirmation = cleaned.get("confirm_password")
        if password and confirmation and password != confirmation:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        candidate = super().save(commit=False)
        candidate.state = self.cleaned_data.get("state") or ""
        candidate.password = make_password(self.cleaned_data["password"])
        if commit:
            candidate.save()
        return candidate


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autocomplete": "username", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}))


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["resume_file"]
        widgets = {"resume_file": forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".pdf,.docx"})}

    def clean_resume_file(self):
        uploaded = self.cleaned_data["resume_file"]
        FileExtensionValidator(["pdf", "docx"])(uploaded)
        if uploaded.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Please upload a file smaller than 10 MB.")
        return uploaded
