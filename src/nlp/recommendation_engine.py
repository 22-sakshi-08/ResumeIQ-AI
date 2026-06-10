import os
import json
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self, skills_db_path: str = None):
        if skills_db_path is None:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            skills_db_path = os.path.join(project_root, 'data', 'skills.json')
            
        self.skills_db_path = skills_db_path
        self.skills_data: Dict[str, dict] = {}
        self._load_skills_db()

    def _load_skills_db(self):
        """Loads the skills database from data/skills.json."""
        if not os.path.exists(self.skills_db_path):
            logger.warning(f"Skills database not found at {self.skills_db_path}. No custom recommendations available.")
            return
            
        try:
            with open(self.skills_db_path, 'r', encoding='utf-8') as f:
                self.skills_data = json.load(f)
            logger.info(f"Loaded {len(self.skills_data)} skills for recommendation lookups.")
        except Exception as e:
            logger.error(f"Failed to load skills database for recommendations: {str(e)}")

    def generate_recommendations(self, gap_analysis: dict) -> List[str]:
        """Generates dynamic recommendations for missing skills using database values.
        
        gap_analysis: dict containing the key 'missing' (list of missing skills)
        """
        missing_skills = gap_analysis.get("missing", [])
        recommendations = []
        
        for skill in missing_skills:
            skill_lower = skill.lower().strip()
            
            # 1. Lookup in skills database
            if skill_lower in self.skills_data:
                rec_text = self.skills_data[skill_lower].get("recommendation")
                if rec_text:
                    recommendations.append(rec_text)
                    continue
            
            # 2. Dynamic fallback template if not found in skills.json
            capitalized_skill = skill.capitalize()
            recommendations.append(f"Strengthen your skills in {capitalized_skill} by building practice projects and review documentation.")
            
        logger.info(f"Generated {len(recommendations)} recommendations for missing skills.")
        return recommendations

if __name__ == "__main__":
    engine = RecommendationEngine()
    recs = engine.generate_recommendations({"missing": ["aws", "docker", "kubernetes", "unknown_skill"]})
    for r in recs:
        print("-", r)
