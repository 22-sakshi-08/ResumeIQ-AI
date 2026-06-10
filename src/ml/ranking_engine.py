import os
import sys
import pickle
import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import CLASSIFIER_PATH, VECTORIZER_PATH, MODELS_DIR, SENTENCE_TRANSFORMER_MODEL
from src.ml.ats_predictor import ATSPredictor
from src.ml.feature_engineering import compute_skill_overlap_score, MASTER_SKILLS

class RankingEngine:
    def __init__(self):
        # Lazy load models when needed
        self.embedding_model = None
        self.classifier = None
        self.vectorizer = None
        self.label_encoder = None
        self.ats_predictor = ATSPredictor()

    def _load_models(self):
        """Loads machine learning and embedding models."""
        if self.embedding_model is None:
            print("Loading Sentence Transformer model...")
            self.embedding_model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
            
        if self.classifier is None:
            if os.path.exists(CLASSIFIER_PATH):
                with open(CLASSIFIER_PATH, 'rb') as f:
                    self.classifier = pickle.load(f)
            else:
                print("Warning: Classification model not trained yet.")
                
        if self.vectorizer is None:
            if os.path.exists(VECTORIZER_PATH):
                with open(VECTORIZER_PATH, 'rb') as f:
                    self.vectorizer = pickle.load(f)
            else:
                print("Warning: TF-IDF Vectorizer not trained yet.")
                
        if self.label_encoder is None:
            le_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
            if os.path.exists(le_path):
                with open(le_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)

    def extract_required_skills(self, jd_text: str) -> list:
        """Helper to extract skills from job description text."""
        jd_text_lower = jd_text.lower()
        extracted = []
        for skill in MASTER_SKILLS:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, jd_text_lower):
                extracted.append(skill)
        return extracted

    def predict_role(self, cleaned_text: str) -> str:
        """Predicts the category/role for a candidate resume."""
        self._load_models()
        if self.classifier is None or self.vectorizer is None or self.label_encoder is None:
            return "Unknown"
        
        # Transform and predict
        tfidf_features = self.vectorizer.transform([cleaned_text]).toarray()
        pred_id = self.classifier.predict(tfidf_features)[0]
        return self.label_encoder.inverse_transform([pred_id])[0]

    def rank_candidates(self, resumes: list, jd_text: str) -> pd.DataFrame:
        """Ranks a list of candidate resumes against a job description.
        
        resumes: list of dicts, each with keys 'resume_id' and 'resume_text' (and optional 'cleaned_text')
        jd_text: raw text of the job description
        """
        self._load_models()
        
        # 1. Process job description
        required_skills = self.extract_required_skills(jd_text)
        jd_embedding = self.embedding_model.encode([jd_text])[0]
        
        candidate_ranks = []
        
        for resume in resumes:
            r_id = resume["resume_id"]
            r_text = resume["resume_text"]
            
            # Clean text fallback
            from src.ml.preprocessor import TextPreprocessor
            preprocessor = TextPreprocessor()
            cleaned_text = resume.get("cleaned_text", preprocessor.preprocess(r_text, use_spacy=False))
            
            # Predict candidate role
            predicted_role = self.predict_role(cleaned_text)
            
            # Predict ATS Score
            ats_res = self.ats_predictor.predict_ats_score(r_text, required_skills=required_skills)
            ats_score = ats_res["ats_score"]
            ats_breakdown = ats_res["breakdown"]
            
            # Compute Skill Match (normalized between 0 and 1)
            skill_match = ats_breakdown["skill_score"] / 40.0
            
            # Compute Semantic Similarity (Cosine on Embeddings)
            resume_embedding = self.embedding_model.encode([r_text])[0]
            semantic_similarity = float(cosine_similarity([resume_embedding], [jd_embedding])[0][0])
            # Normalize negative cosine values if any
            semantic_similarity = max(0.0, semantic_similarity)
            
            # Compute Experience Match (normalized from ATS breakdown)
            experience_match = ats_breakdown["experience_score"] / 25.0
            
            # Compute Education Match (normalized from ATS breakdown)
            education_match = ats_breakdown["education_score"] / 15.0
            
            # Final Score Formula:
            # 0.40 * Skill Match + 0.30 * Semantic Similarity + 0.20 * Experience Match + 0.10 * Education Match
            final_score = (
                0.40 * skill_match +
                0.30 * semantic_similarity +
                0.20 * experience_match +
                0.10 * education_match
            )
            
            candidate_ranks.append({
                "candidate_id": r_id,
                "predicted_role": predicted_role,
                "ats_score": round(ats_score, 1),
                "match_score": round(semantic_similarity * 100, 1), # percentage similarity
                "final_score": round(final_score * 100, 1),         # percentage final score
                "raw_final": final_score
            })
            
        # 2. Sort and assign ranks
        df_ranked = pd.DataFrame(candidate_ranks)
        df_ranked = df_ranked.sort_values(by="raw_final", ascending=False).reset_index(drop=True)
        df_ranked["rank"] = df_ranked.index + 1
        
        # Drop temporary sorting columns
        df_ranked = df_ranked.drop(columns=["raw_final"])
        df_ranked = df_ranked[["candidate_id", "predicted_role", "ats_score", "match_score", "final_score", "rank"]]
        
        # Save to csv
        df_ranked.to_csv("ranked_candidates.csv", index=False)
        print("Saved ranked_candidates.csv")
        return df_ranked

if __name__ == "__main__":
    # Test the Ranking Engine locally
    engine = RankingEngine()
    
    # We must train the classifier before running ranker
    sample_resumes = [
        {
            "resume_id": "RES_001",
            "resume_text": "John Doe. Machine learning engineer with PyTorch, AWS, Python. 5 years experience."
        },
        {
            "resume_id": "RES_002",
            "resume_text": "Alice Smith. Business analyst with Jira, Scrum, Excel. Requirements gathering."
        }
    ]
    
    jd = "Seeking a Machine Learning Engineer experienced in Python, PyTorch, and cloud AWS deployments."
    
    try:
        ranks = engine.rank_candidates(sample_resumes, jd)
        print(ranks)
    except Exception as e:
        print("Test run failed (model may not be pre-trained yet):", str(e))
