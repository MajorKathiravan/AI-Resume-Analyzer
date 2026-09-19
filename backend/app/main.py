from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.resume_extractor import extract_text_from_pdf
from app.services.resume_analyzer import analyze_resume
from app.services.job_analyzer import analyze_job_description
from app.services.job_intelligence import extract_job_intelligence
from app.services.matcher import match_resume_to_job
from app.services.semantic_matcher import calculate_semantic_similarity
from app.services.recommendation_engine import generate_recommendations
from app.services.llm_analyzer import generate_llm_analysis
from app.services.job_fit import calculate_job_fit_score

# Database
from app.services.database import (
    initialize_database,
    save_analysis,
    get_analysis_history,
    get_analysis_by_id,
    delete_analysis,
    update_analysis_result
)


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="AI Resume Analyzer",
    description="AI-powered Resume Analysis and Job Matching API",
    version="1.0.0"
)


# ==========================================
# Initialize Database
# ==========================================

initialize_database()


# ==========================================
# React Frontend → FastAPI
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Upload Directory
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# Request Models
# ==========================================

class JobDescriptionRequest(BaseModel):
    job_description: str


class MatchRequest(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is running"
    }


# ==========================================
# Upload Resume
# ==========================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    safe_filename = Path(file.filename or "").name

    if not safe_filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid file name."
        )

    file_path = UPLOAD_DIR / safe_filename

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    extracted_text = extract_text_from_pdf(
        str(file_path)
    )

    analysis = analyze_resume(
        extracted_text
    )

    return {
        "filename": safe_filename,
        "message": "Resume analyzed successfully",
        "analysis": analysis
    }


# ==========================================
# Analyze Job Description
# ==========================================

@app.post("/analyze-job")
async def analyze_job(
    request: JobDescriptionRequest
):

    if not request.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    analysis = analyze_job_description(
        request.job_description
    )

    return {
        "message": "Job description analyzed successfully",
        "analysis": analysis
    }


# ==========================================
# Match Resume Skills
# ==========================================

@app.post("/match")
def match_resume(
    request: MatchRequest
):

    result = match_resume_to_job(
        request.resume_skills,
        request.job_skills
    )

    return {
        "message": "Resume and job matched successfully",
        "result": result
    }


# ==========================================
# Analysis History
# ==========================================

@app.get("/history")
def analysis_history():

    history = get_analysis_history()

    return {
        "message": "Analysis history retrieved successfully",
        "history": history
    }


# ==========================================
# Analysis History Details
# ==========================================

@app.get("/history/{analysis_id}")
def analysis_details(
    analysis_id: int
):

    result = get_analysis_by_id(
        analysis_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return {
        "message": "Analysis retrieved successfully",
        "analysis": result
    }


# ==========================================
# Delete Analysis History
# ==========================================

@app.delete("/history/{analysis_id}")
def delete_analysis_history(
    analysis_id: int
):

    deleted = delete_analysis(
        analysis_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return {
        "message": "Analysis deleted successfully",
        "analysis_id": analysis_id
    }


# ==========================================
# Complete Resume + Job Analysis
# ==========================================

@app.post("/analyze-resume-match")
async def analyze_resume_match(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # ==========================================
    # Validation
    # ==========================================

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )


    # ==========================================
    # Save Resume
    # ==========================================

    safe_filename = Path(file.filename or "").name

    if not safe_filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid file name."
        )

    file_path = UPLOAD_DIR / safe_filename

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)


    # ==========================================
    # Extract Resume Text
    # ==========================================

    resume_text = extract_text_from_pdf(
        str(file_path)
    )


    # ==========================================
    # Resume Analysis
    # ==========================================

    resume_analysis = analyze_resume(
        resume_text
    )


    # ==========================================
    # Job Description Analysis
    # ==========================================

    job_analysis = analyze_job_description(
        job_description
    )


    # ==========================================
    # Job Intelligence
    # ==========================================

    job_intelligence = extract_job_intelligence(
        job_description
    )


    # ==========================================
    # Keyword Matching
    # ==========================================

    match_result = match_resume_to_job(
        resume_analysis["skills"],
        job_analysis["required_skills"]
    )


    # ==========================================
    # Semantic AI Matching
    # ==========================================

    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )


    # ==========================================
    # Overall Job Fit Score
    # ==========================================

    job_fit = calculate_job_fit_score(
        match_result["match_percentage"],
        semantic_score
    )


    # ==========================================
    # Recommendations
    # ==========================================

    recommendations = generate_recommendations(
        resume_analysis["skills"],
        job_analysis["required_skills"],
        match_result["missing_skills"]
    )


    # ==========================================
    # LLM Analysis
    # ==========================================

    try:

        llm_analysis = generate_llm_analysis(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=match_result[
                "matched_skills"
            ],
            missing_skills=match_result[
                "missing_skills"
            ],
            keyword_score=match_result[
                "match_percentage"
            ],
            semantic_score=semantic_score,
            overall_score=job_fit[
                "overall_score"
            ],
            fit_level=job_fit[
                "level"
            ]
        )

    except Exception as error:

        llm_analysis = {
            "model": "llama3.2",
            "analysis": "LLM analysis is currently unavailable.",
            "error": str(error)
        }


    # ==========================================
    # Save Analysis to Database
    # ==========================================

    analysis_id = save_analysis(
        filename=safe_filename,
        job_title=job_intelligence.get(
            "job_title",
            "Unknown"
        ),
        keyword_score=match_result[
            "match_percentage"
        ],
        semantic_score=semantic_score,
        overall_score=job_fit[
            "overall_score"
        ],
        fit_level=job_fit[
            "level"
        ],
        matched_skills=", ".join(
            match_result["matched_skills"]
        ),
        missing_skills=", ".join(
            match_result["missing_skills"]
        )
    )


    # ==========================================
    # Final Response
    # ==========================================

    final_response = {

        "message": "Resume and job analyzed successfully",

        "analysis_id": analysis_id,


        # --------------------------------------
        # Resume
        # --------------------------------------

        "resume": {

            "filename":
                safe_filename,

            "skills":
                resume_analysis["skills"],

            "text_length":
                resume_analysis["text_length"]
        },


        # --------------------------------------
        # Job
        # --------------------------------------

        "job": {

            "required_skills":
                job_analysis["required_skills"],

            "job_title":
                job_intelligence["job_title"],

            "detected_skills":
                job_intelligence["detected_skills"],

            "experience_requirement":
                job_intelligence[
                    "experience_requirement"
                ],

            "education_requirements":
                job_intelligence[
                    "education_requirements"
                ],

            "text_length":
                job_analysis["text_length"]
        },


        # --------------------------------------
        # Match
        # --------------------------------------

        "match": {

            **match_result,

            "semantic_similarity_score":
                semantic_score,

            "overall_job_fit":
                job_fit
        },


        # --------------------------------------
        # Recommendations
        # --------------------------------------

        "recommendations":
            recommendations,


        # --------------------------------------
        # LLM
        # --------------------------------------

        "llm_analysis":
            llm_analysis
    }


    # ==========================================
    # Save Complete Result to Database
    # ==========================================

    update_analysis_result(
        analysis_id=analysis_id,
        result=final_response
    )


    return final_response
