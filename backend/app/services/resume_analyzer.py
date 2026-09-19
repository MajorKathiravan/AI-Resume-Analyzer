import re

from app.services.skill_extractor import extract_skills


def analyze_resume(text: str) -> dict:

    skills = extract_skills(text)

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return {
        "skills": skills,
        "email": email[0] if email else None,
        "text_length": len(text)
    }