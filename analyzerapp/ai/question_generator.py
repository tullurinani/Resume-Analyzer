def generate_questions(parsed_resume):
    questions = []

    skills = parsed_resume.get("skills", [])
    education = parsed_resume.get("education", [])
    experience = parsed_resume.get("experience", [])

    # Skill-based questions
    if "Python" in skills:
        questions.append("Tell me about your experience with Python.")
    if "Machine Learning" in skills:
        questions.append("Describe a machine learning project you've done.")
    if "Django" in skills:
        questions.append("What projects have you built using Django?")
    if "SQL" in skills:
        questions.append("How proficient are you with writing SQL queries?")
    if "JavaScript" in skills:
        questions.append("Have you used JavaScript for any frontend or backend projects?")
    if "Communication" in skills:
        questions.append("How do you rate your communication skills in a team environment?")

    # Education-based question
    if education:
        questions.append(f"What did you learn during your {education[0]}?")

    # Experience-based questions
    if experience:
        questions.append(f"You mentioned {experience[0]}. Can you elaborate?")
        questions.append("What was your role in that organization?")
        questions.append("What challenges did you face in your previous job and how did you overcome them?")
        questions.append("Which achievement are you most proud of from your past job?")

    # Fallback questions if no meaningful data
    if not questions:
        questions = [
            "Can you walk me through your resume?",
            "What are your key strengths relevant to this role?",
            "Describe a challenge you faced and how you overcame it.",
            "Why are you interested in this position?",
            "Where do you see yourself in five years?",
            "Can you describe a successful project you worked on?",
            "How do you handle working under pressure?"
        ]

    return "\n".join(questions)
