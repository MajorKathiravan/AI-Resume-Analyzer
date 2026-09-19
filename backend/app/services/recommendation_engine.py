def generate_recommendations(
    resume_skills: list,
    job_skills: list,
    missing_skills: list
) -> dict:

    recommendations = []

    if missing_skills:
        recommendations.append(
            "Consider adding experience or projects related to: "
            + ", ".join(missing_skills)
        )

    if "machine learning" in missing_skills:
        recommendations.append(
            "Add at least one Machine Learning project to strengthen the resume."
        )

    if "aws" in missing_skills:
        recommendations.append(
            "Consider learning AWS fundamentals and adding a cloud-based project."
        )

    if "docker" in missing_skills:
        recommendations.append(
            "Add Docker experience by containerizing a Python or FastAPI application."
        )

    if "fastapi" in missing_skills:
        recommendations.append(
            "Build or mention a REST API project using FastAPI."
        )

    if "nlp" in missing_skills:
        recommendations.append(
            "Consider adding an NLP project such as text classification or a chatbot."
        )

    return {
        "recommendations": recommendations,
        "skills_to_improve": missing_skills
    }