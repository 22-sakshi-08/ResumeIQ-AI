import os
import sys
import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.search.embedding_engine import EmbeddingEngine
from src.search.vector_store import VectorStore
from src.search.similarity_engine import SimilarityEngine
from src.nlp.skill_gap_analyzer import SkillGapAnalyzer
from src.ml.ats_predictor import ATSPredictor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobMatcher:
    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.similarity_engine = SimilarityEngine(self.embedding_engine)
        self.gap_analyzer = SkillGapAnalyzer()
        self.ats_predictor = ATSPredictor()

    def match_resume_to_jobs(self, resume_text: str, jobs: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Queries jobs using FAISS vector store and returns Top-K matched jobs."""
        if not jobs:
            return []
            
        # 1. Build temporary Vector Store
        store = VectorStore(dimension=384)
        job_texts = [j.get("jd_text", "") for j in jobs]
        embeddings = self.embedding_engine.encode_batch(job_texts)
        
        # Metadata must include titles and ids
        metadata = [{"job_id": j.get("job_id"), "job_title": j.get("job_title"), "jd_text": j.get("jd_text")} for j in jobs]
        store.build_index(embeddings, metadata)
        
        # 2. Query vector store
        resume_embedding = self.embedding_engine.encode_text(resume_text)
        raw_results = store.search(resume_embedding, top_k=top_k)
        
        # 3. Format results
        formatted = []
        for meta, score in raw_results:
            formatted.append({
                "job_id": meta["job_id"],
                "job_title": meta["job_title"],
                "similarity": round(score, 4)
            })
        return formatted

    def match_job_to_candidates(self, job_description: str, resumes: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
        """Queries resumes using FAISS vector store and returns Top-K matched candidates."""
        if not resumes:
            return []
            
        # 1. Build temporary Vector Store
        store = VectorStore(dimension=384)
        resume_texts = [r.get("resume_text", "") for r in resumes]
        embeddings = self.embedding_engine.encode_batch(resume_texts)
        
        metadata = [{"candidate_id": r.get("candidate_id"), "resume_text": r.get("resume_text")} for r in resumes]
        store.build_index(embeddings, metadata)
        
        # 2. Query vector store
        jd_embedding = self.embedding_engine.encode_text(job_description)
        raw_results = store.search(jd_embedding, top_k=top_k)
        
        # 3. Format results
        formatted = []
        for meta, score in raw_results:
            formatted.append({
                "candidate_id": meta["candidate_id"],
                "similarity": round(score, 4)
            })
        return formatted

    def compute_hybrid_score(self, resume_text: str, jd_text: str) -> Dict[str, float]:
        """Calculates a hybrid matching score combining:
        
        - 40% Semantic Similarity
        - 30% ATS Score
        - 20% Skill Match %
        - 10% Experience Match
        """
        # 1. Semantic Similarity (0.0 to 1.0)
        sim_res = self.similarity_engine.compute_similarity(resume_text, jd_text)
        semantic_similarity = sim_res["similarity"]
        
        # 2. Skill Extraction & Gap Analysis
        from src.nlp.skill_extractor import SkillExtractor
        extractor = SkillExtractor()
        r_skills = extractor.extract_skills(resume_text)
        jd_skills = extractor.extract_skills(jd_text)
        
        gap_res = self.gap_analyzer.analyze(r_skills, jd_skills)
        skill_match_pct = gap_res["match_percentage"] # 0 to 100
        
        # 3. ATS Score & Experience Match
        # Pass Jd skills to ATS Predictor for relevance
        ats_res = self.ats_predictor.predict_ats_score(resume_text, required_skills=jd_skills)
        ats_score = ats_res["ats_score"] # 0 to 100
        exp_score = ats_res["breakdown"]["experience_score"] # 0 to 25
        
        # Normalize scores to 0-1 range
        semantic_ratio = semantic_similarity
        ats_ratio = ats_score / 100.0
        skill_ratio = skill_match_pct / 100.0
        exp_ratio = exp_score / 25.0
        
        # Hybrid formula
        final_ratio = (
            0.40 * semantic_ratio +
            0.30 * ats_ratio +
            0.20 * skill_ratio +
            0.10 * exp_ratio
        )
        
        return {
            "semantic_score": round(semantic_similarity * 100, 1),
            "ats_score": round(ats_score, 1),
            "skill_match": round(skill_match_pct, 1),
            "experience_score": round((exp_score / 25.0) * 100, 1),
            "final_score": round(final_ratio * 100, 1)
        }

    def rank_candidates(self, resumes: List[Dict[str, Any]], jd_text: str) -> List[Dict[str, Any]]:
        """Ranks a list of candidate resumes against a single job description using the hybrid score."""
        ranked = []
        for r in resumes:
            scores = self.compute_hybrid_score(r["resume_text"], jd_text)
            ranked.append({
                "candidate_id": r["candidate_id"],
                **scores
            })
        # Sort descending by final score
        ranked = sorted(ranked, key=lambda x: x["final_score"], reverse=True)
        # Assign ranks
        for idx, item in enumerate(ranked):
            item["rank"] = idx + 1
        return ranked

    def rank_jobs(self, resume_text: str, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ranks a list of job descriptions against a single resume using the hybrid score."""
        ranked = []
        for j in jobs:
            scores = self.compute_hybrid_score(resume_text, j["jd_text"])
            ranked.append({
                "job_id": j["job_id"],
                "job_title": j["job_title"],
                **scores
            })
        # Sort descending
        ranked = sorted(ranked, key=lambda x: x["final_score"], reverse=True)
        # Assign ranks
        for idx, item in enumerate(ranked):
            item["rank"] = idx + 1
        return ranked

if __name__ == "__main__":
    matcher = JobMatcher()
    
    # Simple verification test
    resume = "Python developer with machine learning experience using PyTorch. 5 years experience."
    jobs_list = [
        {
            "job_id": "JOB_001",
            "job_title": "ML Engineer",
            "jd_text": "Required: Python, PyTorch, machine learning. 5 years experience."
        },
        {
            "job_id": "JOB_002",
            "job_title": "HR Manager",
            "jd_text": "Seeking HR recruiter with communication and screening experience."
        }
    ]
    
    res = matcher.rank_jobs(resume, jobs_list)
    print(res)
