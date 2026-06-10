import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "phase" in data
    assert "framework" in data

def test_predict_role_endpoint():
    payload = {
        "resume_text": "Machine Learning Engineer with Python and PyTorch experience building deep neural networks."
    }
    response = client.post("/predict-role", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_role" in data
    assert "confidence" in data
    assert isinstance(data["predicted_role"], str)
    assert isinstance(data["confidence"], float)

def test_predict_role_empty_input():
    payload = {"resume_text": ""}
    response = client.post("/predict-role", json=payload)
    assert response.status_code == 400

def test_ats_score_endpoint():
    payload = {
        "resume_text": "Experienced React developer with HTML, CSS, JavaScript, TypeScript, Git.",
        "required_skills": ["React", "TypeScript", "AWS"]
    }
    response = client.post("/ats-score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ats_score" in data
    assert "breakdown" in data
    assert isinstance(data["ats_score"], float)
    assert 0 <= data["ats_score"] <= 100
    assert "skill_score" in data["breakdown"]

def test_extract_skills_endpoint():
    payload = {"text": "Experienced with Python, AWS, Docker and Kubernetes."}
    response = client.post("/extract-skills", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert isinstance(data["skills"], list)
    assert "python" in data["skills"]
    assert "docker" in data["skills"]

def test_job_match_endpoint():
    payload = {
        "resume_text": "Experienced Python developer with machine learning experience using PyTorch. 5 years experience.",
        "jobs": [
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
        ],
        "top_k": 2
    }
    response = client.post("/job-match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "top_jobs" in data
    assert len(data["top_jobs"]) == 2
    assert data["top_jobs"][0]["job_id"] == "JOB_1"
    assert "final_score" in data["top_jobs"][0]

def test_candidate_match_endpoint():
    payload = {
        "job_description": "Seeking Python developer with machine learning experience using PyTorch.",
        "resumes": [
            {
                "candidate_id": "CAND_1",
                "resume_text": "Experienced Python developer with machine learning using PyTorch. 5 years experience."
            },
            {
                "candidate_id": "CAND_2",
                "resume_text": "HR Recruiter specializing in talent sourcing and interview coordination."
            }
        ],
        "top_k": 2
    }
    response = client.post("/candidate-match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "top_candidates" in data
    assert len(data["top_candidates"]) == 2
    assert data["top_candidates"][0]["candidate_id"] == "CAND_1"
    assert "final_score" in data["top_candidates"][0]

def test_recommendations_endpoint():
    payload = {
        "resume_skills": ["python", "docker", "git"],
        "jd_skills": ["python", "docker", "kubernetes", "aws"]
    }
    response = client.post("/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "matched" in data
    assert "missing" in data
    assert "extra" in data
    assert "match_percentage" in data
    assert "recommendations" in data
    
    assert data["matched"] == ["docker", "python"]
    assert data["missing"] == ["aws", "kubernetes"]
    assert data["match_percentage"] == 50.0
    assert len(data["recommendations"]) == 2
