import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search.semantic_pipeline import analyze_and_match

def test_analyze_and_match_flow():
    resume = "Experienced Python developer with machine learning experience using PyTorch. 5 years experience."
    jobs = [
        {
            "job_id": "JOB_1",
            "job_title": "ML Engineer",
            "jd_text": "Required: Python, PyTorch, machine learning. 5 years experience."
        },
        {
            "job_id": "JOB_2",
            "job_title": "HR Recruiter",
            "jd_text": "HR recruiter, talent acquisition specialist, hiring pipeline."
        }
    ]
    
    result = analyze_and_match(resume, jobs, top_k=2)
    
    assert "ats_score" in result
    assert "skills" in result
    assert "top_jobs" in result
    assert "recommendations" in result
    assert "metrics" in result
    
    # Verify values and types
    assert isinstance(result["skills"], list)
    assert len(result["skills"]) > 0
    
    assert isinstance(result["top_jobs"], list)
    assert len(result["top_jobs"]) == 2
    assert result["top_jobs"][0]["job_id"] == "JOB_1"
    
    # Verify recommendations
    assert isinstance(result["recommendations"], list)
    
    # Verify metrics
    metrics = result["metrics"]
    assert "embedding_time" in metrics
    assert "search_time" in metrics
    assert "ranking_time" in metrics
    assert "total_time" in metrics
    
    assert isinstance(metrics["embedding_time"], float)
    assert isinstance(metrics["search_time"], float)
    assert isinstance(metrics["ranking_time"], float)
    assert isinstance(metrics["total_time"], float)
