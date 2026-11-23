"""Extract readable text and basic profile signals from PDF / DOCX resumes."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from docx import Document
from pypdf import PdfReader

SKILL_TERMS = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "SQL", "MySQL",
    "PostgreSQL", "Django", "Flask", "Spring Boot", "REST API", "JDBC", "HTML",
    "CSS", "React", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "OpenCV", "SailPoint", "Saviynt", "Active Directory", "LDAP", "AWS", "Azure",
]


def extract_text_from_resume(file_path: str | Path) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        chunks = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(chunks).strip()
    if suffix == ".docx":
        document = Document(str(path))
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
        table_text = [cell.text for table in document.tables for row in table.rows for cell in row.cells]
        return "\n".join(paragraphs + table_text).strip()
    raise ValueError("Only PDF and DOCX resumes are supported.")


def _unique_case_preserving(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.casefold()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def parse_resume_text(text: str) -> dict[str, list[str]]:
    normalized = re.sub(r"\s+", " ", text or "")
    skills = []
    for skill in SKILL_TERMS:
        if re.search(r"(?<![\w+#])" + re.escape(skill) + r"(?![\w+#])", normalized, re.IGNORECASE):
            skills.append(skill)

    experience = re.findall(
        r"\b(?:\d{1,2}\+?\s+years?\s+(?:of\s+)?experience[^.\n]*|experience\s+at\s+[^.\n]+)",
        text or "", flags=re.IGNORECASE,
    )
    education = re.findall(
        r"\b(?:B\.?Tech|B\.?E\.?|Bachelor(?:'s)?|Master(?:'s)?|M\.?Tech|M\.?S\.?|Ph\.?D\.?)[^\n]{0,100}",
        text or "", flags=re.IGNORECASE,
    )
    return {
        "skills": _unique_case_preserving(skills),
        "experience": _unique_case_preserving([item.strip() for item in experience]),
        "education": _unique_case_preserving([item.strip() for item in education]),
    }


def parse_resume(file_path: str | Path) -> dict[str, list[str]]:
    return parse_resume_text(extract_text_from_resume(file_path))
