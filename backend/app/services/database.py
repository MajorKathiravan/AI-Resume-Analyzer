import sqlite3
import json
from pathlib import Path
from datetime import datetime


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "resume_analyzer.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            job_title TEXT,
            keyword_score REAL,
            semantic_score REAL,
            overall_score REAL,
            fit_level TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            result_json TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # -----------------------------------------------------
    # Migration for existing databases
    # -----------------------------------------------------

    columns = connection.execute(
        "PRAGMA table_info(analysis_history)"
    ).fetchall()

    column_names = {
        column["name"]
        for column in columns
    }

    if "result_json" not in column_names:
        connection.execute("""
            ALTER TABLE analysis_history
            ADD COLUMN result_json TEXT
        """)

    connection.commit()
    connection.close()


# =========================================================
# SAVE ANALYSIS
# =========================================================

def save_analysis(
    filename: str,
    job_title: str,
    keyword_score: float,
    semantic_score: float,
    overall_score: float,
    fit_level: str,
    matched_skills: str,
    missing_skills: str
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO analysis_history (
            filename,
            job_title,
            keyword_score,
            semantic_score,
            overall_score,
            fit_level,
            matched_skills,
            missing_skills,
            result_json,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            job_title,
            keyword_score,
            semantic_score,
            overall_score,
            fit_level,
            matched_skills,
            missing_skills,
            None,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    connection.commit()

    analysis_id = cursor.lastrowid

    connection.close()

    return analysis_id


# =========================================================
# UPDATE COMPLETE ANALYSIS RESULT
# =========================================================

def update_analysis_result(
    analysis_id: int,
    result: dict
):
    connection = get_connection()

    result_json = json.dumps(
        result,
        ensure_ascii=False
    )

    connection.execute(
        """
        UPDATE analysis_history
        SET result_json = ?
        WHERE id = ?
        """,
        (
            result_json,
            analysis_id
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# GET ANALYSIS HISTORY
# =========================================================

def get_analysis_history():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM analysis_history
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# GET ANALYSIS BY ID
# =========================================================

def get_analysis_by_id(
    analysis_id: int
):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM analysis_history
        WHERE id = ?
        """,
        (analysis_id,)
    ).fetchone()

    connection.close()

    if not row:
        return None

    analysis = dict(row)

    # -----------------------------------------------------
    # Return complete saved analysis if available
    # -----------------------------------------------------

    if analysis.get("result_json"):
        try:
            return json.loads(
                analysis["result_json"]
            )
        except json.JSONDecodeError:
            pass

    # -----------------------------------------------------
    # Fallback for older history records
    # -----------------------------------------------------

    return analysis


# =========================================================
# DELETE ANALYSIS
# =========================================================

def delete_analysis(
    analysis_id: int
):
    connection = get_connection()

    cursor = connection.execute(
        """
        DELETE FROM analysis_history
        WHERE id = ?
        """,
        (analysis_id,)
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted