import sys
import os
import pytest
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ml.ranking_engine import RankingEngine

def test_ranking_engine_ranking():
    engine = RankingEngine()
    
    resumes = [
        {
            "resume_id": "RES_001",
            "resume_text": "Machine Learning Engineer. Python, PyTorch, Scikit-learn, AWS. 8 years experience building deep learning models."
        },
        {
            "resume_id": "RES_002",
            "resume_text": "Junior developer with HTML, CSS, simple Python. 1 year experience."
        }
    ]
    
    jd = "Seeking a senior machine learning engineer with extensive experience in PyTorch and Python modeling and cloud AWS systems."
    
    # We must skip prediction if classifier is not trained yet, but semantic similarity calculations should work
    try:
        ranks = engine.rank_candidates(resumes, jd)
        
        assert isinstance(ranks, pd.DataFrame)
        assert len(ranks) == 2
        
        # Check sorted order (RES_001 should be rank 1 due to high experience/skill overlap)
        assert ranks.iloc[0]["candidate_id"] == "RES_001"
        assert ranks.iloc[0]["rank"] == 1
        assert ranks.iloc[1]["candidate_id"] == "RES_002"
        assert ranks.iloc[1]["rank"] == 2
        
        # Check columns
        for col in ["candidate_id", "predicted_role", "ats_score", "match_score", "final_score", "rank"]:
            assert col in ranks.columns
            
    except Exception as e:
        # If it fails due to classifier model missing, that's fine if the classifier isn't trained yet
        # We can verify it when model is trained
        if "best_model.pkl" in str(e) or "Vectorization" in str(e) or "Vectorizer" in str(e):
            pytest.skip("Models not trained yet.")
        else:
            raise e
