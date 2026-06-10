import os
import re
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define keyword lists for statistical engineering
EDUCATION_KEYWORDS = ["degree", "bs", "ms", "phd", "bachelor", "master", "university", "college", "btech", "mtech", "doctorate"]
CERTIFICATION_KEYWORDS = ["certified", "certificate", "certification", "aws", "oscp", "comptia", "cissp", "ceh", "pmp", "scrum", "itil", "ccna"]
PROJECT_KEYWORDS = ["project", "github", "code", "build", "deploy", "developed", "implemented", "engineered", "designed", "created", "automated"]

# Load a comprehensive list of technical skills
MASTER_SKILLS = [
    # Languages
    "python", "java", "c++", "go", "rust", "c#", "sql", "javascript", "typescript", "ruby", "bash", "html", "css", "assembly", "julia", "sas", "scala", "kotlin", "swift",
    # Frameworks / Libraries
    "spring boot", "django", "asp.net", "flask", "grpc", "scikit-learn", "sklearn", "pandas", "numpy", "tensorflow", "pytorch", "statsmodels", "keras", "xgboost", 
    "hugging face", "huggingface", "langchain", "llamaindex", "fastapi", "node.js", "express", "ruby on rails", "react", "vue.js", "angular", "next.js", "tailwindcss", 
    "redux", "ansible", "terraform", "puppet", "chef", "cloudformation", "metasploit", "burp suite", "nmap", "wireshark", "snort", "spark", "hadoop", "opencv",
    # Tools / Tech
    "git", "docker", "jira", "maven", "gradle", "ci/cd", "linux", "jupyter", "tableau", "mlflow", "anaconda", "aws", "kubernetes", "tensorboard", "weights & biases", 
    "power bi", "looker", "alteryx", "pinecone", "chromadb", "milvus", "postgresql", "mongodb", "redis", "rabbitmq", "graphql", "webpack", "vite", "figma", "npm", 
    "yarn", "vercel", "github actions", "jenkins", "gitlab ci", "prometheus", "grafana", "azure", "gcp", "ec2", "s3", "lambda", "iam", "splunk", "firewalls", 
    "active directory", "kali linux", "agile", "scrum", "waterfall", "uml", "bpmn", "confluence", "excel", "visio", "powerpoint", "ms project", "unix", "solr"
]

class FeatureExtractor:
    def __init__(self, max_features=1000, ngram_range=(1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vectorizer = TfidfVectorizer(max_features=self.max_features, ngram_range=self.ngram_range)

    def fit_vectorizer(self, corpus):
        """Fits TF-IDF vectorizer on text corpus."""
        self.vectorizer.fit(corpus)
        return self

    def transform_tfidf(self, texts):
        """Transforms text sequence into sparse TF-IDF matrix."""
        return self.vectorizer.transform(texts)

    def save_vectorizer(self, filepath):
        """Saves fitted vectorizer to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"Vectorizer successfully saved to {filepath}")

    def load_vectorizer(self, filepath):
        """Loads vectorizer from disk."""
        with open(filepath, 'rb') as f:
            self.vectorizer = pickle.load(f)
        print(f"Vectorizer successfully loaded from {filepath}")
        return self

    @staticmethod
    def extract_stats(text: str) -> dict:
        """Extracts statistical metrics from a resume string."""
        if not isinstance(text, str) or not text.strip():
            return {
                "word_count": 0,
                "unique_word_count": 0,
                "avg_sentence_length": 0.0,
                "skill_count": 0,
                "education_keyword_count": 0,
                "certification_keyword_count": 0,
                "project_keyword_count": 0
            }
        
        # Tokenize words (lowercase for matching)
        words = re.findall(r'\b[a-zA-Z0-9\#\+\-]+\b', text.lower())
        word_count = len(words)
        unique_word_count = len(set(words))
        
        # Sentences tokenization (split by periods, question marks, newlines)
        sentences = [s.strip() for s in re.split(r'[.!?\n]+', text) if s.strip()]
        sentence_count = len(sentences)
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Keyword count helper
        def count_keyword_matches(words_list, keywords):
            return sum(1 for word in words_list if word in keywords)
            
        education_keyword_count = count_keyword_matches(words, EDUCATION_KEYWORDS)
        certification_keyword_count = count_keyword_matches(words, CERTIFICATION_KEYWORDS)
        project_keyword_count = count_keyword_matches(words, PROJECT_KEYWORDS)
        
        # Skills matching (using skill phrase token search)
        skill_count = 0
        lower_text = text.lower()
        for skill in MASTER_SKILLS:
            # Word boundary check for skills
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, lower_text):
                skill_count += 1
                
        return {
            "word_count": word_count,
            "unique_word_count": unique_word_count,
            "avg_sentence_length": float(avg_sentence_length),
            "skill_count": skill_count,
            "education_keyword_count": education_keyword_count,
            "certification_keyword_count": certification_keyword_count,
            "project_keyword_count": project_keyword_count
        }

    def generate_stats_dataframe(self, df, text_column):
        """Converts text column in a DataFrame to statistical features."""
        stats_list = df[text_column].apply(self.extract_stats).tolist()
        return pd.DataFrame(stats_list)

# Reusable Similarity functions
def compute_cosine_similarity(vec1, vec2):
    """Computes cosine similarity between two 2D vectors/matrices."""
    return cosine_similarity(vec1, vec2)

def compute_jaccard_similarity(text1: str, text2: str) -> float:
    """Computes Jaccard Similarity between two text strings."""
    if not isinstance(text1, str) or not isinstance(text2, str):
        return 0.0
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if not union:
        return 0.0
    return float(len(intersection) / len(union))

def compute_skill_overlap_score(resume_skills: list, required_skills: list) -> float:
    """Calculates ratio of required skills found in candidate skills."""
    if not required_skills:
        return 1.0
    r_skills_lower = [s.lower().strip() for s in required_skills]
    c_skills_lower = [s.lower().strip() for s in resume_skills]
    
    overlap = sum(1 for rs in r_skills_lower if rs in c_skills_lower)
    return float(overlap / len(required_skills))

def compute_keyword_coverage_score(text: str, keywords: list) -> float:
    """Calculates ratio of keywords matched in text."""
    if not keywords:
        return 1.0
    text_lower = text.lower()
    matches = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw.lower().strip()) + r'\b', text_lower))
    return float(matches / len(keywords))
