import os
import json
import logging
import re
from typing import List, Dict, Pattern

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillExtractor:
    def __init__(self, skills_db_path: str = None):
        if skills_db_path is None:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            skills_db_path = os.path.join(project_root, 'data', 'skills.json')
            
        self.skills_db_path = skills_db_path
        self.patterns: Dict[str, List[Pattern]] = {}
        self._load_skills_and_compile_regex()

    def _load_skills_and_compile_regex(self):
        """Loads skills.json and compiles regex patterns for canonical names and aliases."""
        if not os.path.exists(self.skills_db_path):
            logger.warning(f"Skills database not found at {self.skills_db_path}. No patterns compiled.")
            return
            
        try:
            with open(self.skills_db_path, 'r', encoding='utf-8') as f:
                skills_data = json.load(f)
                
            for canonical, info in skills_data.items():
                canonical_lower = canonical.lower().strip()
                self.patterns[canonical_lower] = []
                
                # Gather all terms to match
                terms = [canonical_lower] + [a.lower().strip() for a in info.get("aliases", [])]
                
                for term in terms:
                    # Escape special characters for regex matching
                    escaped = re.escape(term)
                    
                    # Boundary handling for terms containing special characters (e.g. C++, C#, .NET)
                    # If term ends with a non-word character (like + or #), we need custom boundary check:
                    if term == 'c':
                        pattern_str = r'\bc(?![\+#])\b'
                    elif re.search(r'[^a-zA-Z0-9]$', term):
                        pattern_str = r'\b' + escaped + r'(?:\s|$|[.,;!?:])'
                    else:
                        pattern_str = r'\b' + escaped + r'\b'
                        
                    compiled = re.compile(pattern_str, re.IGNORECASE)
                    self.patterns[canonical_lower].append(compiled)
                    
            logger.info(f"Successfully compiled regex patterns for {len(self.patterns)} skills.")
        except Exception as e:
            logger.error(f"Failed to compile skill extraction patterns: {str(e)}")

    def extract_skills(self, text: str) -> List[str]:
        """Extracts a unique, sorted list of canonical skills found in the text using regex."""
        if not isinstance(text, str) or not text.strip():
            return []
            
        found_skills = set()
        
        # Clean text slightly (normalize spaces)
        cleaned_text = re.sub(r'\s+', ' ', text)
        
        # Search for each skill in text
        for canonical, regex_list in self.patterns.items():
            for regex in regex_list:
                if regex.search(cleaned_text):
                    found_skills.add(canonical)
                    break # Already matched this canonical skill, move to next
                    
        return sorted(list(found_skills))

if __name__ == "__main__":
    extractor = SkillExtractor()
    sample_text = "Experienced Python developer with AWS, Docker and Kubernetes experience. Also knows C++."
    extracted = extractor.extract_skills(sample_text)
    print("Input:", sample_text)
    print("Output:", extracted)
