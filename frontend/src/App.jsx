import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);

  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  const [error, setError] = useState("");

  // =========================================================
  // LOAD HISTORY
  // =========================================================

  const loadHistory = async (openPanel = true) => {
    setHistoryLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/history`);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load analysis history."
        );
      }

      if (Array.isArray(data)) {
        setHistory(data);
      } else if (Array.isArray(data.history)) {
        setHistory(data.history);
      } else if (Array.isArray(data.analyses)) {
        setHistory(data.analyses);
      } else {
        setHistory([]);
      }

      if (openPanel) {
        setShowHistory(true);
      }
    } catch (error) {
      console.error("History error:", error);

      setError(
        error.message ||
          "Unable to load analysis history."
      );
    } finally {
      setHistoryLoading(false);
    }
  };

  // Load history once when application starts
  useEffect(() => {
    const timer = setTimeout(() => {
      loadHistory(false);
    }, 0);

    return () => clearTimeout(timer);
  }, []);

  // =========================================================
  // ANALYZE RESUME
  // =========================================================

  const analyzeResume = async () => {
    if (!file) {
      setError("Please select a PDF resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("file", file);
    formData.append(
      "job_description",
      jobDescription
    );

    try {
      const response = await fetch(
        `${API_URL}/analyze-resume-match`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Resume analysis failed."
        );
      }

      setResult(data);

      // Refresh history without opening the panel
      loadHistory(false);

      // Scroll to results
      setTimeout(() => {
        window.scrollTo({
          top: 500,
          behavior: "smooth",
        });
      }, 100);
    } catch (error) {
      console.error(
        "Analysis error:",
        error
      );

      setError(
        error.message ||
          "Unable to connect to the FastAPI backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // LOAD SINGLE ANALYSIS
  // =========================================================

  const loadAnalysis = async (analysisId) => {
    if (!analysisId) {
      return;
    }

    setHistoryLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/history/${analysisId}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to load analysis details."
        );
      }

      /*
       * Support both:
       *
       * 1. Direct response
       * 2. { analysis: {...} }
       */

      const analysisData =
        data.analysis &&
        typeof data.analysis === "object"
          ? data.analysis
          : data;

      setResult(analysisData);

      setShowHistory(false);

      setTimeout(() => {
        window.scrollTo({
          top: 500,
          behavior: "smooth",
        });
      }, 100);
    } catch (error) {
      console.error(
        "Analysis details error:",
        error
      );

      setError(
        error.message ||
          "Unable to load analysis details."
      );
    } finally {
      setHistoryLoading(false);
    }
  };

  // =========================================================
  // DELETE ANALYSIS
  // =========================================================

  const deleteAnalysis = async (analysisId) => {
    if (!analysisId) {
      return;
    }

    const confirmed = window.confirm(
      "Are you sure you want to delete this analysis?"
    );

    if (!confirmed) {
      return;
    }

    setHistoryLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/history/${analysisId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to delete analysis."
        );
      }

      setHistory((currentHistory) =>
        currentHistory.filter(
          (item) =>
            (item.analysis_id ?? item.id) !== analysisId
        )
      );

      if (
        result?.analysis_id === analysisId ||
        result?.id === analysisId
      ) {
        setResult(null);
      }

    } catch (error) {
      console.error(
        "Delete analysis error:",
        error
      );

      setError(
        error.message ||
          "Unable to delete analysis."
      );
    } finally {
      setHistoryLoading(false);
    }
  };

  // =========================================================
  // CLEAR ANALYSIS
  // =========================================================

  const clearAnalysis = () => {
    setResult(null);
    setFile(null);
    setJobDescription("");
    setError("");
  };

  // =========================================================
  // FORMAT DATE
  // =========================================================

  const formatDate = (dateValue) => {
    if (!dateValue) {
      return "";
    }

    try {
      return new Date(dateValue).toLocaleString(
        "en-IN",
        {
          dateStyle: "medium",
          timeStyle: "short",
        }
      );
    } catch {
      return dateValue;
    }
  };

  // =========================================================
  // GET HISTORY SCORE
  // =========================================================

  const getHistoryScore = (item) => {
    if (
      typeof item.overall_score === "number"
    ) {
      return item.overall_score;
    }

    if (
      typeof item.overall_job_fit === "number"
    ) {
      return item.overall_job_fit;
    }

    if (
      item.overall_job_fit &&
      typeof item.overall_job_fit === "object"
    ) {
      return item.overall_job_fit.overall_score;
    }

    if (
      typeof item.overall_job_fit_score === "number"
    ) {
      return item.overall_job_fit_score;
    }

    return null;
  };

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="app">

      {/* =====================================================
          HEADER
      ====================================================== */}

      <header className="header">

        <div className="header-content">

          <div className="logo-icon">
            AI
          </div>

          <h1>
            AI Resume Analyzer
          </h1>

          <p>
            Analyze your resume, compare it with a job
            description, and get AI-powered career insights.
          </p>

          {/* HISTORY BUTTON */}

          <button
            type="button"
            className="history-button"
            onClick={() => loadHistory(true)}
            disabled={historyLoading}
          >
            {historyLoading
              ? "Loading History..."
              : "📚 Analysis History"}
          </button>

        </div>

      </header>


      {/* =====================================================
          MAIN
      ====================================================== */}

      <main className="container">


        {/* ===================================================
            HISTORY PANEL
        ==================================================== */}

        {showHistory && (

          <section className="history-panel">

            <div className="history-header">

              <div>

                <h2>
                  📚 Analysis History
                </h2>

                <p>
                  Previous resume analyses stored in the database
                </p>

              </div>

              <button
                type="button"
                className="close-history-button"
                onClick={() =>
                  setShowHistory(false)
                }
              >
                ✕
              </button>

            </div>


            {/* HISTORY LOADING */}

            {historyLoading ? (

              <div className="history-loading">
                Loading analysis history...
              </div>

            ) : history.length === 0 ? (

              /* EMPTY HISTORY */

              <div className="history-empty">

                <span>
                  📂
                </span>

                <h3>
                  No analysis history found
                </h3>

                <p>
                  Analyze a resume to create your
                  first history record.
                </p>

              </div>

            ) : (

              /* HISTORY LIST */

              <div className="history-list">

                {history.map(
                  (item, index) => {

                    const analysisId =
                      item.analysis_id ??
                      item.id;

                    const filename =
                      item.resume_filename ??
                      item.filename ??
                      "Resume Analysis";

                    const jobTitle =
                      item.job_title ??
                      item.jobTitle ??
                      "Job Analysis";

                    const score =
                      getHistoryScore(item);

                    const createdAt =
                      item.created_at ??
                      item.createdAt ??
                      "";

                    return (

                      <div
                        className="history-item"
                        key={
                          analysisId ??
                          index
                        }
                      >

                        {/* LEFT */}

                        <div className="history-item-info">

                          <div className="history-file-icon">
                            📄
                          </div>

                          <div>

                            <h3>
                              {filename}
                            </h3>

                            <p>
                              💼 {jobTitle}
                            </p>

                            {createdAt && (
                              <small>
                                {formatDate(
                                  createdAt
                                )}
                              </small>
                            )}

                          </div>

                        </div>


                        {/* RIGHT */}

                        <div className="history-item-right">

                          {typeof score ===
                            "number" && (

                            <strong>
                              {score}%
                            </strong>

                          )}

                          {analysisId && (
                            <>
                              <button
                                type="button"
                                className="view-history-button"
                                onClick={() =>
                                  loadAnalysis(
                                    analysisId
                                  )
                                }
                              >
                                View
                              </button>

                              <button
                                type="button"
                                className="delete-history-button"
                                onClick={() =>
                                  deleteAnalysis(
                                    analysisId
                                  )
                                }
                              >
                                Delete
                              </button>
                            </>
                          )}

                        </div>

                      </div>

                    );
                  }
                )}

              </div>

            )}

          </section>

        )}


        {/* ===================================================
            INPUT SECTION
        ==================================================== */}

        <section className="input-grid">


          {/* RESUME */}

          <div className="card">

            <div className="card-title">

              <span className="title-icon">
                📄
              </span>

              <div>

                <h2>
                  Upload Resume
                </h2>

                <p>
                  Upload your resume in PDF format
                </p>

              </div>

            </div>


            <label className="upload-box">

              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={(event) => {

                  const selectedFile =
                    event.target.files[0];

                  if (selectedFile) {

                    setFile(selectedFile);
                    setError("");

                  }

                }}
              />


              <div className="upload-content">

                <div className="upload-icon">
                  📄
                </div>

                <strong>
                  {file
                    ? file.name
                    : "Click to upload PDF resume"}
                </strong>

                <span>
                  {file
                    ? "Resume selected successfully"
                    : "PDF files only"}
                </span>

              </div>

            </label>

          </div>


          {/* JOB DESCRIPTION */}

          <div className="card">

            <div className="card-title">

              <span className="title-icon">
                💼
              </span>

              <div>

                <h2>
                  Job Description
                </h2>

                <p>
                  Paste the job description below
                </p>

              </div>

            </div>


            <textarea
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(event) =>
                setJobDescription(
                  event.target.value
                )
              }
            />

          </div>

        </section>


        {/* ===================================================
            ACTION BUTTONS
        ==================================================== */}

        <div className="action-buttons">

          <button
            type="button"
            className="analyze-button"
            onClick={analyzeResume}
            disabled={loading}
          >

            {loading ? (

              <>
                <span className="spinner"></span>
                Analyzing with AI...
              </>

            ) : (

              <>
                🚀 Analyze Resume
              </>

            )}

          </button>


          {result && (

            <button
              type="button"
              className="clear-button"
              onClick={clearAnalysis}
            >
              🔄 New Analysis
            </button>

          )}

        </div>


        {/* ===================================================
            ERROR
        ==================================================== */}

        {error && (

          <div className="error">
            ❌ {error}
          </div>

        )}


        {/* ===================================================
            RESULTS
        ==================================================== */}

        {result && (

          <section className="results">


            {/* RESULTS HEADER */}

            <div className="results-header">

              <h2>
                Analysis Results
              </h2>

              <p>
                Resume analysis completed successfully
              </p>

              {result.analysis_id && (

                <span className="analysis-id">
                  Analysis ID: #{result.analysis_id}
                </span>

              )}

            </div>


            {/* =================================================
                SCORE CARDS
            ================================================== */}

            <div className="score-grid">


              {/* KEYWORD */}

              <div className="score-card">

                <span className="score-icon">
                  🎯
                </span>

                <span className="score-label">
                  Keyword Match
                </span>

                <strong>
                  {result.match?.match_percentage ??
                    0}
                  %
                </strong>

              </div>


              {/* SEMANTIC */}

              <div className="score-card">

                <span className="score-icon">
                  🧠
                </span>

                <span className="score-label">
                  Semantic Similarity
                </span>

                <strong>
                  {result.match
                    ?.semantic_similarity_score ??
                    0}
                  %
                </strong>

              </div>


              {/* MATCHED */}

              <div className="score-card">

                <span className="score-icon">
                  ✅
                </span>

                <span className="score-label">
                  Matched Skills
                </span>

                <strong>
                  {result.match
                    ?.matched_skills?.length ??
                    0}
                </strong>

              </div>


              {/* MISSING */}

              <div className="score-card">

                <span className="score-icon">
                  ⚠️
                </span>

                <span className="score-label">
                  Missing Skills
                </span>

                <strong>
                  {result.match
                    ?.missing_skills?.length ??
                    0}
                </strong>

              </div>


              {/* OVERALL JOB FIT */}

              {result.match?.overall_job_fit && (

                <div className="score-card overall-fit-card">

                  <span className="score-icon">
                    🏆
                  </span>

                  <span className="score-label">
                    Overall Job Fit
                  </span>

                  <strong>
                    {
                      result.match
                        .overall_job_fit
                        .overall_score
                    }
                    %
                  </strong>

                  <span className="fit-level">
                    {
                      result.match
                        .overall_job_fit
                        .level
                    }
                  </span>

                </div>

              )}

            </div>


            {/* =================================================
                MATCHED SKILLS
            ================================================== */}

            <div className="result-card">

              <div className="result-title">

                <span>
                  ✅
                </span>

                <h3>
                  Matched Skills
                </h3>

              </div>


              <div className="skills">

                {result.match?.matched_skills
                  ?.length > 0 ? (

                  result.match.matched_skills.map(
                    (skill) => (

                      <span
                        className="skill matched"
                        key={skill}
                      >
                        {skill}
                      </span>

                    )
                  )

                ) : (

                  <p className="empty-message">
                    No matching skills detected.
                  </p>

                )}

              </div>

            </div>


            {/* =================================================
                MISSING SKILLS
            ================================================== */}

            <div className="result-card">

              <div className="result-title">

                <span>
                  ⚠️
                </span>

                <h3>
                  Missing Skills
                </h3>

              </div>


              <div className="skills">

                {result.match?.missing_skills
                  ?.length > 0 ? (

                  result.match.missing_skills.map(
                    (skill) => (

                      <span
                        className="skill missing"
                        key={skill}
                      >
                        {skill}
                      </span>

                    )
                  )

                ) : (

                  <p className="empty-message">
                    No missing skills detected.
                  </p>

                )}

              </div>

            </div>


            {/* =================================================
                JOB INTELLIGENCE
            ================================================== */}

            {result.job && (

              <div className="result-card job-intelligence-card">

                <div className="result-title">

                  <span>
                    💼
                  </span>

                  <div>

                    <h3>
                      Job Intelligence
                    </h3>

                    <p className="job-intelligence-subtitle">
                      Automatically extracted information
                      from the job description
                    </p>

                  </div>

                </div>


                <div className="job-info">


                  {/* JOB TITLE */}

                  <div className="job-info-item">

                    <span className="job-info-label">
                      Job Title
                    </span>

                    <strong className="job-title-value">

                      {result.job.job_title ||
                        "Not detected"}

                    </strong>

                  </div>


                  {/* EXPERIENCE */}

                  <div className="job-info-item">

                    <span className="job-info-label">
                      Experience Requirement
                    </span>

                    <strong>

                      {result.job
                        .experience_requirement ||
                        "Not specified"}

                    </strong>

                  </div>


                  {/* EDUCATION */}

                  <div className="job-info-item">

                    <span className="job-info-label">
                      Education Requirements
                    </span>

                    <strong>

                      {result.job
                        .education_requirements
                        ?.length > 0
                        ? result.job
                            .education_requirements
                            .join(", ")
                        : "Not specified"}

                    </strong>

                  </div>


                  {/* DETECTED SKILLS */}

                  <div className="job-info-item">

                    <span className="job-info-label">
                      Detected Skills
                    </span>

                    <div className="skills">

                      {result.job
                        .detected_skills
                        ?.length > 0 ? (

                        result.job.detected_skills.map(
                          (skill) => (

                            <span
                              className="skill job-skill"
                              key={skill}
                            >
                              {skill}
                            </span>

                          )
                        )

                      ) : (

                        <p className="empty-message">
                          No skills detected.
                        </p>

                      )}

                    </div>

                  </div>

                </div>

              </div>

            )}


            {/* =================================================
                RECOMMENDATIONS
            ================================================== */}

            {result.recommendations && (

              <div className="result-card">

                <div className="result-title">

                  <span>
                    💡
                  </span>

                  <h3>
                    Recommendations
                  </h3>

                </div>


                {result.recommendations
                  .recommendations
                  ?.length > 0 ? (

                  <ul className="recommendation-list">

                    {result.recommendations
                      .recommendations
                      .map(
                        (recommendation, index) => (

                          <li key={index}>
                            {recommendation}
                          </li>

                        )
                      )}

                  </ul>

                ) : (

                  <p className="empty-message">
                    No recommendations available.
                  </p>

                )}

              </div>

            )}


            {/* =================================================
                AI CAREER ANALYSIS
            ================================================== */}

            {result.llm_analysis && (

              <div className="result-card llm-card">

                <div className="result-title">

                  <span>
                    🤖
                  </span>

                  <div>

                    <h3>
                      AI Career Analysis
                    </h3>

                    <p className="ai-model">
                      Powered by{" "}
                      {result.llm_analysis.model ||
                        "Ollama"}
                    </p>

                  </div>

                </div>


                {result.llm_analysis.analysis ? (

                  <div className="llm-analysis">

                    <ReactMarkdown>
                      {
                        result.llm_analysis
                          .analysis
                      }
                    </ReactMarkdown>

                  </div>

                ) : (

                  <p className="empty-message">
                    AI analysis is currently unavailable.
                  </p>

                )}

              </div>

            )}

          </section>

        )}

      </main>


      {/* =====================================================
          FOOTER
      ====================================================== */}

      <footer>

        <p>
          AI Resume Analyzer
        </p>

        <span>
          Powered by FastAPI + React +
          Sentence Transformers + Ollama
        </span>

      </footer>

    </div>
  );
}

export default App;