import os
import sys
import pytest
import pickle
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import CLASSIFIER_PATH, VECTORIZER_PATH, MODELS_DIR

def test_classifier_predictions():
    # Make sure models exist before verifying (fallback check if test run is done before full training)
    if not os.path.exists(CLASSIFIER_PATH) or not os.path.exists(VECTORIZER_PATH):
        pytest.skip("Models not trained yet. Run train_classifier.py first.")
        
    with open(CLASSIFIER_PATH, 'rb') as f:
        model = pickle.load(f)
        
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
        
    le_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
    with open(le_path, 'rb') as f:
        label_encoder = pickle.load(f)
        
    # Check predicting role
    sample_text = "Experienced machine learning engineer designing neural networks and training transformers using PyTorch."
    features = vectorizer.transform([sample_text]).toarray()
    
    pred = model.predict(features)
    probs = model.predict_proba(features)
    
    assert len(pred) == 1
    assert probs.shape[1] == len(label_encoder.classes_)
    
    pred_label = label_encoder.inverse_transform(pred)[0]
    assert isinstance(pred_label, str)
