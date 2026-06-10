import logging
from typing import List, Dict, Union
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.nlp.skill_normalizer import SkillNormalizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillGapAnalyzer:
    def __init__(self, normalizer: SkillNormalizer = None):
        self.normalizer = normalizer or SkillNormalizer()

    def analyze(self, resume_skills: List[str], jd_skills: List[str]) -> Dict[str, Union[List[str], float]]:
        """Compares resume skills against job description skills.
        
        Calculates matched, missing, and extra skills, along with a match percentage.
        """
        # Normalize both lists to ensure accurate comparisons
        normalized_resume = self.normalizer.normalize_list(resume_skills)
        normalized_jd = self.normalizer.normalize_list(jd_skills)
        
        resume_set = set(normalized_resume)
        jd_set = set(normalized_jd)
        
        # Calculate sets
        matched = sorted(list(resume_set.intersection(jd_set)))
        missing = sorted(list(jd_set.difference(resume_set)))
        extra = sorted(list(resume_set.difference(jd_set)))
        
        # Calculate percentage matching
        if len(jd_set) > 0:
            match_percentage = (len(matched) / len(jd_set)) * 100
        else:
            match_percentage = 100.0
            
        match_percentage = round(match_percentage, 2)
        
        logger.info(f"Skill Gap Analysis completed. Matched: {len(matched)}, Missing: {len(missing)}, Match%: {match_percentage}%")
        
        return {
            "matched": matched,
            "missing": missing,
            "extra": extra,
            "match_percentage": float(match_percentage)
        }

if __name__ == "__main__":
    analyzer = SkillGapAnalyzer()
    res = analyzer.analyze(["python", "aws", "docker"], ["python", "aws", "kubernetes"])
    print(res)
