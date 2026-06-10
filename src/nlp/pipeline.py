import os
import sys
import logging
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.nlp.skill_extractor import SkillExtractor
from src.nlp.skill_normalizer import SkillNormalizer
from src.nlp.skill_gap_analyzer import SkillGapAnalyzer
from src.nlp.recommendation_engine import RecommendationEngine
from src.ml.ats_predictor import ATSPredictor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPIntegrationPipeline:
    def __init__(self):
        self.extractor = SkillExtractor()
        self.normalizer = SkillNormalizer()
        self.gap_analyzer = SkillGapAnalyzer(self.normalizer)
        self.recommender = RecommendationEngine()
        self.ats_predictor = ATSPredictor()

    def analyze_resume_against_jd(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Integrates all Phase 4 modules with the Phase 3 ATSPredictor.
        
        Runs extraction, normalization, gap analysis, ATS scoring, and recommendations.
        """
        logger.info("Starting integrated resume and job description analysis pipeline...")
        
        # 1. Skill Extraction
        resume_raw_skills = self.extractor.extract_skills(resume_text)
        jd_raw_skills = self.extractor.extract_skills(jd_text)
        
        # 2. Skill Normalization
        resume_skills = self.normalizer.normalize_list(resume_raw_skills)
        jd_skills = self.normalizer.normalize_list(jd_raw_skills)
        
        # 3. Skill Gap Analysis
        gap_analysis = self.gap_analyzer.analyze(resume_skills, jd_skills)
        
        # 4. ATS Score Prediction (integrating Phase 3 predictor)
        # We pass jd_skills as the required skills to let the predictor compute overlap
        ats_result = self.ats_predictor.predict_ats_score(resume_text, required_skills=jd_skills)
        ats_score = ats_result["ats_score"]
        
        # 5. Recommendation Generation
        recommendations = self.recommender.generate_recommendations(gap_analysis)
        
        pipeline_output = {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "matched": gap_analysis["matched"],
            "missing": gap_analysis["missing"],
            "extra": gap_analysis["extra"],
            "match_percentage": gap_analysis["match_percentage"],
            "ats_score": ats_score,
            "recommendations": recommendations
        }
        
        logger.info("Integrated analysis pipeline run completed successfully.")
        return pipeline_output

def analyze_resume_against_jd(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """Top-level helper function for pipeline analysis."""
    pipeline = NLPIntegrationPipeline()
    return pipeline.analyze_resume_against_jd(resume_text, jd_text)

if __name__ == "__main__":
    resume = """
    Jane Developer
    jane.dev@gmail.com
    Skills: Python, React, PostgreSQL, Git, Docker.
    5 years experience.
    """
    
    jd = """
    Required Skills:
    Python, AWS, React, Docker, Kubernetes.
    """
    
    res = analyze_resume_against_jd(resume, jd)
    print("MATCH PERCENTAGE:", res["match_percentage"])
    print("ATS SCORE:", res["ats_score"])
    print("RECOMMENDATIONS:")
    for rec in res["recommendations"]:
        print("-", rec)
