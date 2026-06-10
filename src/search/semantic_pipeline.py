import os
import sys
import time
import logging
from typing import List, Dict, Any

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.search.embedding_engine import EmbeddingEngine
from src.search.job_matcher import JobMatcher
from src.nlp.skill_extractor import SkillExtractor
from src.nlp.skill_normalizer import SkillNormalizer
from src.nlp.skill_gap_analyzer import SkillGapAnalyzer
from src.nlp.recommendation_engine import RecommendationEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticPipeline:
    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.job_matcher = JobMatcher()
        self.skill_extractor = SkillExtractor()
        self.normalizer = SkillNormalizer()
        self.gap_analyzer = SkillGapAnalyzer(self.normalizer)
        self.recommender = RecommendationEngine()

    def analyze_and_match(self, resume_text: str, jobs: List[Dict[str, Any]], top_k: int = 5) -> Dict[str, Any]:
        """Runs the end-to-end semantic analysis and job matching pipeline.
        
        Pipeline Steps:
        1. Extract resume skills.
        2. Encode resume embedding (timed).
        3. Query FAISS search for semantic ranking (timed).
        4. Compute hybrid rank scores for all jobs (timed).
        5. Compile top job matches and dynamic recommendations for the best match.
        """
        logger.info("Starting Semantic Job Matching Pipeline...")
        start_total = time.time()
        
        # 1. Skill Extraction from Resume
        resume_raw_skills = self.skill_extractor.extract_skills(resume_text)
        resume_skills = self.normalizer.normalize_list(resume_raw_skills)
        
        # 2. Embedding Generation (Time it)
        embed_start = time.time()
        # Single encode
        _ = self.embedding_engine.encode_text(resume_text)
        # Batch encode jobs
        job_texts = [j.get("jd_text", "") for j in jobs]
        _ = self.embedding_engine.encode_batch(job_texts)
        embedding_time = time.time() - embed_start
        
        # 3. FAISS Search & Retrieval (Time it)
        search_start = time.time()
        # This will use FAISS search to get candidate-job similarity
        _ = self.job_matcher.match_resume_to_jobs(resume_text, jobs, top_k=top_k)
        search_time = time.time() - search_start
        
        # 4. Hybrid Scoring & Ranking (Time it)
        ranking_start = time.time()
        ranked_jobs = self.job_matcher.rank_jobs(resume_text, jobs)
        ranking_time = time.time() - ranking_start
        
        # 5. Extract top matching job and calculate recommendations
        top_job = {}
        recommendations = []
        ats_score = 0.0
        
        # Cap top_jobs to top_k
        ranked_jobs = ranked_jobs[:top_k]
        
        if ranked_jobs:
            top_job = ranked_jobs[0]
            ats_score = top_job.get("ats_score", 0.0)
            
            # Get matching JD text
            jd_id = top_job.get("job_id")
            jd_text = next((j.get("jd_text", "") for j in jobs if j.get("job_id") == jd_id), "")
            
            # Get skill gap recommendations
            jd_raw_skills = self.skill_extractor.extract_skills(jd_text)
            jd_skills = self.normalizer.normalize_list(jd_raw_skills)
            gap_res = self.gap_analyzer.analyze(resume_skills, jd_skills)
            recommendations = self.recommender.generate_recommendations(gap_res)
            
        total_time = time.time() - start_total
        logger.info(f"Pipeline finished in {total_time:.3f}s. "
                    f"Embedding: {embedding_time:.3f}s, "
                    f"Search: {search_time:.3f}s, "
                    f"Ranking: {ranking_time:.3f}s")
                    
        return {
            "ats_score": ats_score,
            "skills": resume_skills,
            "top_jobs": ranked_jobs,
            "recommendations": recommendations,
            "metrics": {
                "embedding_time": round(embedding_time, 4),
                "search_time": round(search_time, 4),
                "ranking_time": round(ranking_time, 4),
                "total_time": round(total_time, 4)
            }
        }

def analyze_and_match(resume_text: str, jobs: List[Dict[str, Any]], top_k: int = 5) -> Dict[str, Any]:
    """Helper module function wrapper for end-to-end execution."""
    pipeline = SemanticPipeline()
    return pipeline.analyze_and_match(resume_text, jobs, top_k=top_k)

if __name__ == "__main__":
    resume = "Experienced Python developer with machine learning experience using PyTorch. 5 years experience."
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
    
    res = analyze_and_match(resume, jobs_list)
    print("Pipeline Results:")
    print("ATS Score:", res["ats_score"])
    print("Skills:", res["skills"])
    print("Top Jobs:", res["top_jobs"])
    print("Recommendations:", res["recommendations"])
    print("Metrics:", res["metrics"])
