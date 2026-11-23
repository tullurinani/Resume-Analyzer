"""Generate explainable, rule-based interview prompts from resume fields."""
from __future__ import annotations


def generate_questions(parsed_resume: dict) -> list[str]:
    questions: list[str] = []
    skills = parsed_resume.get("skills", [])
    education = parsed_resume.get("education", [])
    experience = parsed_resume.get("experience", [])

    prompts = {
        "Python": "Can you explain a Python project where you used functions, data structures or file handling?",
        "Java": "Which object-oriented programming concepts have you used in Java, and where?",
        "SQL": "Describe an SQL query where you used joins, grouping or a subquery. How did you validate its result?",
        "Django": "How does Django handle a request from a URL to a view and then to a template?",
        "Spring Boot": "How would you design a REST endpoint in Spring Boot and validate its input?",
        "Machine Learning": "How did you split your dataset and evaluate your machine-learning model?",
        "TensorFlow": "How did you prepare your data and avoid overfitting when training a model?",
        "OpenCV": "Which image-processing steps did you use before running your computer-vision logic?",
        "Saviynt": "How would you explain the relationship between an identity, an account and an entitlement in an IGA platform?",
        "SailPoint": "How would you troubleshoot an account aggregation that is not correlating to the expected identity?",
        "JDBC": "How would you troubleshoot a JDBC connection or account-import failure?",
        "REST API": "How do you handle an unsuccessful REST API response and decide whether to retry?",
    }
    for skill in skills:
        for key, question in prompts.items():
            if str(skill).casefold() == key.casefold():
                questions.append(question)
                break

    if education:
        questions.append(f"What is one practical concept you applied during your studies in {education[0]}?")
    if experience:
        questions.append(f"You listed {experience[0]}. What was your specific contribution and outcome?")
    questions.extend([
        "Walk me through one project from problem statement to final result.",
        "Describe a technical issue you faced, how you investigated it and how you verified the fix.",
    ])
    return questions[:10]
