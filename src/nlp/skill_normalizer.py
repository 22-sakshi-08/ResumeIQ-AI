import os
import json
import logging
import re
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillNormalizer:
    def __init__(self, skills_db_path: str = None):
        if skills_db_path is None:
            # Point to default data/skills.json
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            skills_db_path = os.path.join(project_root, 'data', 'skills.json')
            
        self.skills_db_path = skills_db_path
        self.normalization_map: Dict[str, str] = {}
        self._load_skills_db()

    def _load_skills_db(self):
        """Loads skills database and builds a normalization map from aliases and canonical names."""
        if not os.path.exists(self.skills_db_path):
            logger.warning(f"Skills database not found at {self.skills_db_path}. Normalizing will use standard fallbacks.")
            return
            
        try:
            with open(self.skills_db_path, 'r', encoding='utf-8') as f:
                skills_data = json.load(f)
                
            for canonical, info in skills_data.items():
                canonical_lower = canonical.lower().strip()
                # Map canonical to itself
                self.normalization_map[canonical_lower] = canonical_lower
                
                # Map aliases to canonical
                aliases = info.get("aliases", [])
                for alias in aliases:
                    alias_lower = alias.lower().strip()
                    self.normalization_map[alias_lower] = canonical_lower
                    
            logger.info(f"Loaded {len(skills_data)} skills with {len(self.normalization_map)} normalization mapping entries.")
        except Exception as e:
            logger.error(f"Failed to load skills database: {str(e)}")

    def normalize(self, skill: str) -> str:
        """Normalizes a raw skill string into its canonical form.
        
        Handles casing, spacing, punctuation, and synonym/alias mapping.
        """
        if not isinstance(skill, str) or not skill.strip():
            return ""
            
        # 1. Basic Cleaning
        cleaned = skill.lower().strip()
        
        # Replace hyphens/underscores with space for synonym checking (e.g. "machine-learning" -> "machine learning")
        cleaned_space = re.sub(r'[\-_]+', ' ', cleaned).strip()
        
        # 2. Check direct mapping
        if cleaned in self.normalization_map:
            return self.normalization_map[cleaned]
            
        if cleaned_space in self.normalization_map:
            return self.normalization_map[cleaned_space]
            
        # 3. Handle specific punctuation variations (e.g., stripping dots: "node.js" -> "node.js" or "node js")
        # Check if stripping dots matches (e.g., "node.js" -> "nodejs" or "node js")
        cleaned_no_dot = cleaned.replace(".", "")
        if cleaned_no_dot in self.normalization_map:
            return self.normalization_map[cleaned_no_dot]
            
        # 4. Fallback: return cleaned space version
        return cleaned_space

    def normalize_list(self, skills: List[str]) -> List[str]:
        """Normalizes a list of raw skill strings and removes duplicates while preserving order."""
        if not skills:
            return []
            
        normalized = []
        seen = set()
        for skill in skills:
            norm_skill = self.normalize(skill)
            if norm_skill and norm_skill not in seen:
                seen.add(norm_skill)
                normalized.append(norm_skill)
                
        return normalized

if __name__ == "__main__":
    normalizer = SkillNormalizer()
    print("PyTorch ->", normalizer.normalize("PyTorch"))
    print("ML ->", normalizer.normalize("ML"))
    print("machine-learning ->", normalizer.normalize("machine-learning"))
    print("JS ->", normalizer.normalize("JS"))
    print("javascript ->", normalizer.normalize("javascript"))
    print("List normalization ->", normalizer.normalize_list(["PyTorch", "PyTorch", "ML", "python"]))
