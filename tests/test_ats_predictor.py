import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ml.ats_predictor import ATSPredictor

def test_ats_predictor_score():
    predictor = ATSPredictor()
    
    resume_text = """
    Software Developer
    Python, Javascript, Git, Docker, Kubernetes.
    Led team to design scalable database solutions.
    Master of Science in Computer Science.
    Certified Kubernetes Administrator.
    """
    
    res = predictor.predict_ats_score(resume_text, required_skills=["Python", "Docker"])
    
    # Check that score exists and is bounded between 0 and 100
    assert "ats_score" in res
    assert 0 <= res["ats_score"] <= 100
    
    # Check details and breakdowns
    assert "breakdown" in res
    breakdown = res["breakdown"]
    assert "skill_score" in breakdown
    assert "experience_score" in breakdown
    assert "projects_score" in breakdown
    assert "education_score" in breakdown
    
    # Check bounds of individual sub-scores
    assert 0 <= breakdown["skill_score"] <= 40
    assert 0 <= breakdown["experience_score"] <= 25
    assert 0 <= breakdown["projects_score"] <= 20
    assert 0 <= breakdown["education_score"] <= 15
    
    # Final score is sum of parts
    expected_sum = (
        breakdown["skill_score"] + 
        breakdown["experience_score"] + 
        breakdown["projects_score"] + 
        breakdown["education_score"]
    )
    assert abs(res["ats_score"] - expected_sum) < 0.1
