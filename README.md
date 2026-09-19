# 🤖 AI Resume Analyzer & Job Matcher

> An AI-powered career assistant that analyzes resumes, understands job descriptions, identifies skill gaps, calculates job-fit scores, and provides AI-powered career insights.

**React** • **FastAPI** • **Python** • **Machine Learning** • **NLP** • **Generative AI** • **SQLite**

---

## 🌟 Overview

AI Resume Analyzer & Job Matcher is a full-stack AI application designed to help job seekers understand how well their resume matches a specific job description.

The system combines keyword matching, semantic similarity, job intelligence, recommendations, and Generative AI to provide a detailed analysis of the resume against the target job.

The application provides both structured matching results and AI-generated career insights in a single workflow.

---

## ✨ Features

### 📄 Resume Analysis

- Upload resumes in PDF format
- Extract resume text using PyMuPDF
- Detect relevant technical skills
- Analyze resume content
- Extract available contact information

### 💼 Job Description Analysis

- Enter a job description
- Detect required technical skills
- Identify relevant technologies
- Analyze job requirements
- Extract available job intelligence

### 🔗 Resume–Job Matching

- Keyword-based skill matching
- Matched skills identification
- Missing skills identification
- Semantic similarity matching
- Combined job-fit score

### 🤖 Generative AI

- AI-powered resume analysis
- Resume strengths
- Job-fit explanation
- Missing skill explanation
- Resume improvement suggestions
- Interview preparation tips
- Powered by Ollama and Llama 3.2

### 💾 Analysis History

- Save completed analyses
- Store results in SQLite
- View previous analyses
- Restore complete analysis results
- Delete saved analyses

### 🌐 Full-Stack Application

- React frontend
- FastAPI backend
- REST API integration
- Swagger / OpenAPI documentation
- Responsive user interface

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │     React Frontend      │
                    │       Web Interface     │
                    └────────────┬────────────┘
                                 │
                                 │ REST API
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Backend    │
                    │         Python          │
                    └────────────┬────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
     Resume Analysis       Job Analysis        Matching Engine
            │                    │                    │
            ▼                    ▼             ┌──────┴──────┐
         PyMuPDF          Skill Detection      │             │
                                               ▼             ▼
                                         Keyword Match  Semantic Match
                                               │             │
                                               └──────┬──────┘
                                                      │
                                                      ▼
                                            Job Fit Calculation
                                                      │
                     ┌────────────────────────────────┼──────────────────┐
                     │                                │                  │
                     ▼                                ▼                  ▼
               Recommendations                    SQLite             Ollama
                                                 History            Llama 3.2
```

---

## 🛠️ Technology Stack

### Frontend

- React
- JavaScript
- React Markdown
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### AI / Machine Learning

- Sentence Transformers
- Semantic Similarity
- Scikit-learn
- Ollama
- Llama 3.2

### PDF / Data Processing

- PyMuPDF
- Python

### Database

- SQLite

### API

- REST API
- Swagger / OpenAPI

---

## 📁 Project Structure

```text
AI-Resume-Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── resume_extractor.py
│   │       ├── resume_analyzer.py
│   │       ├── job_analyzer.py
│   │       ├── matcher.py
│   │       ├── semantic_matcher.py
│   │       ├── recommendation_engine.py
│   │       ├── llm_analyzer.py
│   │       ├── job_fit.py
│   │       ├── job_intelligence.py
│   │       └── database.py
│   │
│   ├── requirements.txt
│   └── uploads/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

## 🔄 Application Workflow

```text
1. Upload Resume
        ↓
2. Extract PDF Text
        ↓
3. Analyze Resume
        ↓
4. Detect Resume Skills
        ↓
5. Analyze Job Description
        ↓
6. Detect Required Skills
        ↓
7. Keyword Matching
        ↓
8. Semantic Similarity Matching
        ↓
9. Job Intelligence Analysis
        ↓
10. Job Fit Score Calculation
        ↓
11. Identify Missing Skills
        ↓
12. Generate Recommendations
        ↓
13. Generate Llama 3.2 AI Analysis
        ↓
14. Save Analysis to SQLite
        ↓
15. Display Complete Results
```

---

## 📊 Job Fit Scoring

The application combines two matching signals:

| Matching Signal | Weight |
|---|---:|
| Keyword Match | 50% |
| Semantic Similarity | 50% |

### Formula

```text
Overall Score =
    (Keyword Score × 0.50)
    +
    (Semantic Score × 0.50)
```

### Fit Levels

| Score | Fit Level |
|---:|---|
| 80–100 | Excellent Match |
| 65–79 | Strong Match |
| 50–64 | Moderate Match |
| 35–49 | Partial Match |
| 0–34 | Low Match |

> **Note:** The job-fit score is an application-level heuristic based on the implemented matching signals. It is not a prediction of hiring probability or a guarantee of job selection.

---

## 🧠 Semantic Matching

The application uses Sentence Transformers to compare the semantic similarity between resume content and job-description content.

This allows the system to consider contextual similarity rather than relying only on exact keyword overlap.

```text
Resume Text
     │
     ▼
Sentence Transformer
     │
     ▼
Resume Embedding
     │
     │ Compare
     │
     ▼
Job Description Embedding
     ▲
     │
Sentence Transformer
     │
     ▼
Job Description
     │
     ▼
Semantic Similarity Score
```

---

## 🔍 Keyword Matching

The keyword matching component compares the skills detected in the resume with the skills detected in the job description.

The system identifies:

- ✅ Matched Skills
- ❌ Missing Skills
- 📊 Keyword Match Percentage

```text
Resume Skills
      │
      ▼
Resume Skill Set
      │
      │ Intersection
      ▼
Matched Skills
      ▲
      │
Job Skill Set
      ▲
      │
Job Description Skills
```

---

## 💼 Job Intelligence

The job intelligence layer analyzes the job description and extracts information such as:

- Job title
- Detected skills
- Experience requirements
- Education requirements

This information provides additional context for the overall resume-to-job analysis.

---

## 💡 Recommendations

The recommendation engine uses the matching results to identify areas where the resume can be improved.

Recommendations can focus on:

- Missing technical skills
- Resume alignment
- Skills to strengthen
- Interview preparation areas
- Job-specific improvement opportunities

---

## 🤖 Generative AI

The application integrates **Ollama + Llama 3.2** for additional AI-powered analysis.

The AI generates the following sections:

### 1. Resume Strengths

Identifies strengths supported by the resume.

### 2. Job Fit Explanation

Explains how the resume aligns with the provided job description.

### 3. Missing Skills

Highlights skills detected in the job description but not in the resume.

### 4. Resume Improvement Suggestions

Provides suggestions for improving the resume based on the target job.

### 5. Interview Preparation Tips

Provides preparation topics based on the resume and job description.

The LLM prompt instructs the model to focus on information supported by the resume and job description and avoid inventing experience or qualifications.

---

## 🧠 AI / ML Pipeline

```text
Resume Text
     │
     ├── Skill Extraction
     │
     ├── Keyword Analysis
     │
     └── Semantic Representation
                │
                ▼
         Job Description
                │
                ├── Skill Extraction
                │
                ├── Keyword Analysis
                │
                └── Semantic Representation
                         │
                         ▼
                  Matching Engine
                         │
                ┌────────┴────────┐
                ▼                 ▼
          Keyword Score     Semantic Score
                │                 │
                └────────┬────────┘
                         ▼
                   Job Fit Score
                         │
                         ▼
                    AI Analysis
```

---

## 💾 Analysis History

Completed analyses are stored in a local **SQLite database**.

The system stores:

- Resume filename
- Job title
- Keyword match score
- Semantic similarity score
- Overall job-fit score
- Fit level
- Matched skills
- Missing skills
- Complete analysis result
- Creation timestamp

### History Operations

```text
New Analysis
     │
     ▼
Save Analysis
     │
     ├──────────────► View
     │
     └──────────────► Delete
```

Users can view previous analyses and restore complete saved results.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API health/home endpoint |
| `POST` | `/upload-resume` | Upload and process a resume |
| `POST` | `/analyze-job` | Analyze a job description |
| `POST` | `/match` | Match resume skills with job skills |
| `GET` | `/history` | Retrieve analysis history |
| `GET` | `/history/{analysis_id}` | Retrieve a saved analysis |
| `DELETE` | `/history/{analysis_id}` | Delete a saved analysis |
| `POST` | `/analyze-resume-match` | Run complete resume-to-job analysis |

---

## 📚 Swagger API Documentation

FastAPI provides interactive Swagger documentation for the backend API.

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to inspect and test the available API endpoints.

---

## ⚙️ Backend Setup

### 1. Navigate to the backend

```powershell
cd "D:\VS Code\AI-Resume-Analyzer\backend"
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Start the FastAPI server

```powershell
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger URL:

```text
http://127.0.0.1:8000/docs
```

---

## 💻 Frontend Setup

Open a second terminal.

### 1. Navigate to the frontend

```powershell
cd "D:\VS Code\AI-Resume-Analyzer\frontend"
```

### 2. Install dependencies

```powershell
npm install
```

### 3. Start the development server

```powershell
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 🦙 Ollama Setup

The Generative AI analysis feature uses **Ollama** with **Llama 3.2**.

Download the model:

```powershell
ollama pull llama3.2
```

Make sure Ollama is running before using the AI analysis feature.

The backend communicates with:

```text
http://localhost:11434/api/generate
```

---

## 🧪 Testing

The complete application workflow has been tested successfully.

### Backend

- ✅ FastAPI startup
- ✅ Swagger documentation
- ✅ Resume PDF upload
- ✅ Resume text extraction
- ✅ Job description analysis
- ✅ Keyword matching
- ✅ Semantic matching
- ✅ Job-fit calculation
- ✅ Missing skill detection
- ✅ Job intelligence

### Generative AI

- ✅ Ollama integration
- ✅ Llama 3.2 analysis
- ✅ Resume strengths
- ✅ Job-fit explanation
- ✅ Missing skills
- ✅ Resume improvement suggestions
- ✅ Interview preparation tips

### Database

- ✅ SQLite history
- ✅ Save analysis
- ✅ View analysis
- ✅ Restore complete analysis
- ✅ Delete analysis

### Frontend

- ✅ React application
- ✅ Frontend/backend integration
- ✅ Analysis workflow
- ✅ Result display
- ✅ Analysis history
- ✅ View functionality
- ✅ Delete functionality
- ✅ Responsive interface

---

## 🔐 Repository Hygiene

The following local and generated files are excluded from Git:

```text
venv/
backend/venv/
backend/uploads/
uploads/
*.db
*.sqlite
*.sqlite3
.env
.env.*
__pycache__/
*.pyc
*.pyo
.vscode/
*.log
```

This helps prevent local environments, uploaded resumes, local databases, environment files, and generated files from being committed accidentally.

---

## 🚀 Future Improvements

Potential future enhancements include:

- OCR support for scanned resumes
- More advanced resume section extraction
- Expanded skill taxonomy
- Job recommendation engine
- Multiple resume comparison
- Resume scoring improvements
- Authentication and user accounts
- Cloud deployment
- Job-board integrations
- Advanced analytics dashboard

---

## 🎯 Project Objective

This project demonstrates how to build a complete AI-powered product by combining:

- Artificial Intelligence
- Machine Learning
- Natural Language Processing
- Generative AI
- Semantic Similarity
- Python
- FastAPI
- React
- REST APIs
- SQLite
- AI-assisted career analysis

The project is designed as a portfolio project demonstrating **AI Product Development and full-stack AI application engineering**.

---

## 👨‍💻 Author

### Kathiravan Velmurugan

**B.Tech – Artificial Intelligence & Data Science**

**AI / ML • Generative AI • Python • FastAPI • React • Data Science**

---

## ⭐ Project

**AI Resume Analyzer & Job Matcher**

Built as an **AI Product Development portfolio project**.
