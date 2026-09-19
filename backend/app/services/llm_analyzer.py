import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def generate_llm_analysis(
    resume_text: str,
    job_description: str,
    matched_skills: list,
    missing_skills: list,
    keyword_score: float,
    semantic_score: float,
    overall_score: float,
    fit_level: str
) -> dict:

    matched_text = (
        ", ".join(matched_skills)
        if matched_skills
        else "None"
    )

    missing_text = (
        ", ".join(missing_skills)
        if missing_skills
        else "None"
    )

    prompt = f"""
You are an AI career assistant inside a Resume Analyzer application.

Analyze the resume against the job description using the calculated results
provided by the application.

IMPORTANT RULES:

1. The calculated results are authoritative.
2. Do NOT recalculate any score.
3. Do NOT invent skills, experience, projects, or qualifications.
4. Do NOT contradict the matched skills.
5. Do NOT say a matched skill is missing.
6. The Missing Skills section MUST contain ONLY the skills listed in
   the provided Missing Skills list.
7. If the Missing Skills list contains one or more skills, explicitly list
   those skills.
8. If the Missing Skills list is empty, say:
   "No major missing skills were detected."
9. Use the provided overall job fit score and level exactly.
10. Base the analysis only on the provided resume, job description,
    and calculated results.

==================================================
CALCULATED ANALYSIS RESULTS
==================================================

Keyword Match Score:
{keyword_score}%

Semantic Similarity Score:
{semantic_score}%

Overall Job Fit Score:
{overall_score}%

Overall Job Fit Level:
{fit_level}

Matched Skills:
{matched_text}

Missing Skills:
{missing_text}

==================================================
RESUME
==================================================

{resume_text}

==================================================
JOB DESCRIPTION
==================================================

{job_description}

==================================================
OUTPUT FORMAT
==================================================

## 1. Resume Strengths

Explain the strongest relevant skills, education, projects,
certifications, and experience found in the resume.

## 2. Job Fit Explanation

Explain how the matched skills relate to the job description.

Mention the calculated:

- Keyword Match Score
- Semantic Similarity Score
- Overall Job Fit Score
- Overall Job Fit Level

Do not change these values.

## 3. Missing Skills

If missing skills are provided, list ONLY those skills.

For example:

- NLP

Do not add any other skills.

If there are no missing skills, say:

No major missing skills were detected.

## 4. Resume Improvement Suggestions

Provide practical suggestions based specifically on the missing skills
and the job description.

Do not claim that the candidate already has a missing skill.

## 5. Interview Preparation Tips

Provide interview preparation suggestions based on:

- The job description
- The matched skills
- The missing skills
- The candidate's actual resume

Do not invent experience.

==================================================

Remember:

The application-calculated results are authoritative.

Matched skills must remain matched.

Missing skills must remain missing.

Never contradict the calculated results.
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return {
        "model": MODEL,
        "analysis": data.get("response", "").strip()
    }