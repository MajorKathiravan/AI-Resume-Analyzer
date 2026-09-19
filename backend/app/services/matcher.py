def match_resume_to_job(resume_skills: list, job_skills: list) -> dict:

    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    matched_skills = sorted(resume_set.intersection(job_set))
    missing_skills = sorted(job_set - resume_set)

    if job_set:
        match_percentage = round(
            (len(matched_skills) / len(job_set)) * 100,
            2
        )
    else:
        match_percentage = 0

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": len(job_set),
        "total_matched_skills": len(matched_skills)
    }