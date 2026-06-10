import os
import sys
import logging
from typing import List, Dict, Any

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

class CandidateMatcher:
    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.similarity_engine = SimilarityEngine(self.embedding_engine)
        self.gap_analyzer = SkillGapAnalyzer()
        self.ats_predictor = ATSPredictor()

    def match_job_to_candidates(self, job_description: str, resumes: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
        """Queries resumes using FAISS vector store and returns Top-K matched candidates.
        
        Args:
            job_description (str): Text of the job description.
            resumes (List[Dict]): List of resume dicts containing "candidate_id" and "resume_text".
            top_k (int): Number of candidates to return.
            
        Returns:
            List[Dict]: Ranked list of candidates with similarity scores.
        """
        if not resumes:
            logger.warning("Empty candidate list passed to CandidateMatcher.")
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
        from src.search.job_matcher import JobMatcher
        matcher = JobMatcher()
        return matcher.compute_hybrid_score(resume_text, jd_text)

    def rank_candidates(self, resumes: List[Dict[str, Any]], jd_text: str) -> List[Dict[str, Any]]:
        """Ranks a list of candidate resumes against a single job description using the hybrid score.
        
        Args:
            resumes (List[Dict]): Resumes with "candidate_id" and "resume_text".
            jd_text (str): Job description text.
            
        Returns:
            List[Dict]: Ranked list of candidates with hybrid score breakdown.
        """
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

if __name__ == "__main__":
    matcher = CandidateMatcher()
    
    # Simple verification test
    jd = "Seeking a Python developer with machine learning experience using PyTorch."
    candidates = [
        {
            "candidate_id": "CAND_001",
            "resume_text": "Experienced Python developer with machine learning using PyTorch. 5 years experience."
        },
        {
            "candidate_id": "CAND_002",
            "resume_text": "HR Recruiter specializing in talent sourcing and interview coordination."
        }
    ]
    
    res = matcher.rank_candidates(candidates, jd)
    print("Ranked Candidates:", res)
