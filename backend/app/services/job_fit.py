def calculate_job_fit_score(
    keyword_score: float,
    semantic_score: float
) -> dict:

    overall_score = (
        keyword_score * 0.50
        + semantic_score * 0.50
    )

    overall_score = round(overall_score, 2)

    if overall_score >= 80:
        level = "Excellent Match"
    elif overall_score >= 65:
        level = "Strong Match"
    elif overall_score >= 50:
        level = "Moderate Match"
    elif overall_score >= 35:
        level = "Partial Match"
    else:
        level = "Low Match"

    return {
        "overall_score": overall_score,
        "level": level,
        "keyword_weight": 50,
        "semantic_weight": 50
    }