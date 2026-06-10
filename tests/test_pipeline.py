import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nlp.pipeline import analyze_resume_against_jd

def test_pipeline_integration():
    resume = """
    John Doe
    john@example.com
    Skills: Python, PyTorch, Docker, PostgreSQL, git.
    Working as a Machine Learning Engineer with 5 years experience.
    """
    
    jd = """
    Looking for a Senior ML Engineer.
    Must have Python, PyTorch, AWS, Docker, Kubernetes.
    """
    
    res = analyze_resume_against_jd(resume, jd)
    
    # Check fields
    assert "resume_skills" in res
    assert "jd_skills" in res
    assert "matched" in res
    assert "missing" in res
    assert "extra" in res
    assert "match_percentage" in res
    assert "ats_score" in res
    assert "recommendations" in res
    
    # Check extraction values (canonical form checks)
    assert "python" in res["resume_skills"]
    assert "pytorch" in res["resume_skills"]
    assert "docker" in res["resume_skills"]
    
    assert "python" in res["jd_skills"]
    assert "pytorch" in res["jd_skills"]
    assert "aws" in res["jd_skills"]
    assert "kubernetes" in res["jd_skills"]
    
    # Check gap metrics
    # Required in JD: python, pytorch, aws, docker, kubernetes (5 required)
    # Matched: python, pytorch, docker (3 matched)
    # Missing: aws, kubernetes (2 missing)
    # Match percentage = 3 / 5 * 100 = 60.0%
    assert res["matched"] == ["docker", "python", "pytorch"]
    assert res["missing"] == ["aws", "kubernetes"]
    assert res["match_percentage"] == 60.0
    
    # Check ATS score is bounded
    assert 0 <= res["ats_score"] <= 100
    
    # Check recommendations (should be 2, for aws and kubernetes)
    assert len(res["recommendations"]) == 2
    assert any("aws" in r.lower() or "cloud" in r.lower() for r in res["recommendations"])
    assert any("kubernetes" in r.lower() or "orchestration" in r.lower() for r in res["recommendations"])
