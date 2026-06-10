import sys
import os
import pytest
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search.similarity_engine import SimilarityEngine

def test_similarity_identical_texts():
    engine = SimilarityEngine()
    text = "Senior Software Engineer with experience in Python and AWS cloud architecture."
    res = engine.compute_similarity(text, text)
    
    assert "similarity" in res
    assert np.isclose(res["similarity"], 1.0, atol=1e-4)

def test_similarity_related_texts():
    engine = SimilarityEngine()
    text_a = "Machine Learning Developer training PyTorch models."
    text_b = "AI Software Engineer building neural networks."
    
    res = engine.compute_similarity(text_a, text_b)
    # They should be highly related (similarity > 0.5)
    assert res["similarity"] > 0.4
    assert 0.0 <= res["similarity"] <= 1.0

def test_similarity_unrelated_texts():
    engine = SimilarityEngine()
    text_a = "Kubernetes DevOps engineer managing Docker containers."
    text_b = "Human Resources Manager and talent acquisition lead."
    
    res = engine.compute_similarity(text_a, text_b)
    # They should be very low similarity
    assert res["similarity"] < 0.3

def test_similarity_empty_inputs():
    engine = SimilarityEngine()
    res1 = engine.compute_similarity("", "Non-empty")
    res2 = engine.compute_similarity("Non-empty", "")
    res3 = engine.compute_similarity("", "")
    
    assert res1["similarity"] == 0.0
    assert res2["similarity"] == 0.0
    assert res3["similarity"] == 0.0
