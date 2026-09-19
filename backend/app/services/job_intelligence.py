import re


def extract_job_intelligence(text: str) -> dict:
    text_lower = text.lower()

    job_title = None

    title_patterns = [
        r"looking for a ([^.]+?) with",
        r"hiring a ([^.]+?) with",
        r"seeking a ([^.]+?) with",
        r"position[:\-]\s*([^\n]+)",
        r"role[:\-]\s*([^\n]+)"
    ]

    for pattern in title_patterns:
        match = re.search(pattern, text_lower)

        if match:
            job_title = match.group(1).strip()
            break

    skills = [
        "python",
        "java",
        "javascript",
        "sql",
        "mysql",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "fastapi",
        "react",
        "aws",
        "docker",
        "power bi",
        "pandas",
        "numpy",
        "nlp",
        "llm",
        "openai",
        "api",
        "cloud",
        "data processing",
        "automation"
    ]

    detected_skills = [
        skill
        for skill in skills
        if skill in text_lower
    ]

    experience = None

    experience_patterns = [
        r"(\d+\+?\s*years?)\s+(?:of\s+)?experience",
        r"experience\s+of\s+(\d+\+?\s*years?)"
    ]

    for pattern in experience_patterns:
        match = re.search(pattern, text_lower)

        if match:
            experience = match.group(1)
            break

    education_keywords = [
        "bachelor",
        "b.tech",
        "b.e",
        "master",
        "m.tech",
        "m.e",
        "degree",
        "computer science",
        "information technology",
        "artificial intelligence",
        "data science"
    ]

    education = [
        item
        for item in education_keywords
        if item in text_lower
    ]

    return {
        "job_title": job_title,
        "detected_skills": detected_skills,
        "experience_requirement": experience,
        "education_requirements": education,
        "text_length": len(text)
    }