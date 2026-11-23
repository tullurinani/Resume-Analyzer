from django.contrib import admin
from django.utils.html import format_html

from .models import Candidate, Resume


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "state", "status", "submitted_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("status", "state")
    readonly_fields = ("submitted_at",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("candidate", "uploaded_at", "download_resume")
    search_fields = ("candidate__name", "candidate__email")
    readonly_fields = ("uploaded_at",)

    @admin.display(description="Resume file")
    def download_resume(self, obj):
        if obj.resume_file:
            return format_html('<a href="{}" target="_blank" rel="noopener">Open file</a>', obj.resume_file.url)
        return "No file"
