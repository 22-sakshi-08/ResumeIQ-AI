import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search.job_matcher import JobMatcher
from src.search.candidate_matcher import CandidateMatcher

@pytest.fixture
def mock_data():
    resume = "Experienced Python developer with machine learning experience using PyTorch. 5 years experience."
    resumes = [
        {
            "candidate_id": "CAND_1",
            "resume_text": "Experienced Python developer with machine learning using PyTorch. 5 years experience."
        },
        {
            "candidate_id": "CAND_2",
            "resume_text": "HR Recruiter specializing in talent sourcing and interview coordination."
        }
    ]
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
    return resume, resumes, jobs

def test_match_resume_to_jobs(mock_data):
    resume, _, jobs = mock_data
    matcher = JobMatcher()
    
    top_jobs = matcher.match_resume_to_jobs(resume, jobs, top_k=2)
    assert len(top_jobs) == 2
    assert top_jobs[0]["job_id"] == "JOB_1"
    assert top_jobs[0]["similarity"] > top_jobs[1]["similarity"]

def test_match_job_to_candidates(mock_data):
    _, resumes, jobs = mock_data
    matcher = CandidateMatcher()
    
    top_candidates = matcher.match_job_to_candidates(jobs[0]["jd_text"], resumes, top_k=2)
    assert len(top_candidates) == 2
    assert top_candidates[0]["candidate_id"] == "CAND_1"
    assert top_candidates[0]["similarity"] > top_candidates[1]["similarity"]

def test_compute_hybrid_score(mock_data):
    resume, _, jobs = mock_data
    matcher = JobMatcher()
    
    score_res = matcher.compute_hybrid_score(resume, jobs[0]["jd_text"])
    
    assert "semantic_score" in score_res
    assert "ats_score" in score_res
    assert "skill_match" in score_res
    assert "experience_score" in score_res
    assert "final_score" in score_res
    
    # Test formula: 0.4*semantic + 0.3*ats + 0.2*skill_match + 0.1*exp
    expected = (
        0.4 * score_res["semantic_score"] +
        0.3 * score_res["ats_score"] +
        0.2 * score_res["skill_match"] +
        0.1 * score_res["experience_score"]
    )
    assert abs(score_res["final_score"] - expected) < 0.5

def test_rank_jobs(mock_data):
    resume, _, jobs = mock_data
    matcher = JobMatcher()
    
    ranked = matcher.rank_jobs(resume, jobs)
    assert len(ranked) == 2
    assert ranked[0]["job_id"] == "JOB_1"
    assert ranked[0]["rank"] == 1
    assert ranked[1]["job_id"] == "JOB_2"
    assert ranked[1]["rank"] == 2

def test_rank_candidates(mock_data):
    _, resumes, jobs = mock_data
    matcher = CandidateMatcher()
    
    ranked = matcher.rank_candidates(resumes, jobs[0]["jd_text"])
    assert len(ranked) == 2
    assert ranked[0]["candidate_id"] == "CAND_1"
    assert ranked[0]["rank"] == 1
    assert ranked[1]["candidate_id"] == "CAND_2"
    assert ranked[1]["rank"] == 2
