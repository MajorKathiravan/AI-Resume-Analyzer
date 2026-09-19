from app.services.skill_extractor import extract_skills


def analyze_job_description(text: str) -> dict:

    required_skills = extract_skills(text)

    text_lower = text.lower()

    responsibilities = []

    responsibility_keywords = [
        "develop",
        "design",
        "build",
        "implement",
        "maintain",
        "analyze",
        "create",
        "deploy",
        "test",
        "integrate",
        "manage",
        "optimize",
        "automate",
    ]

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        line_lower = line.lower()

        if any(
            keyword in line_lower
            for keyword in responsibility_keywords
        ):
            responsibilities.append(line)

    return {
        "required_skills": required_skills,
        "responsibilities": responsibilities,
        "text_length": len(text)
    }