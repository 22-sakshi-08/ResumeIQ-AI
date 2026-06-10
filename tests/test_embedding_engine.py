import sys
import os
import numpy as np
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search.embedding_engine import EmbeddingEngine

def test_singleton_pattern():
    engine1 = EmbeddingEngine()
    engine2 = EmbeddingEngine()
    assert engine1 is engine2

def test_encode_single_text():
    engine = EmbeddingEngine()
    text = "Machine Learning Engineer"
    vec = engine.encode_text(text)
    
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (384,)
    # Verify L2 normalization
    assert np.isclose(np.linalg.norm(vec), 1.0, atol=1e-5)

def test_encode_batch_text():
    engine = EmbeddingEngine()
    texts = ["Data Scientist", "Software Developer", "DevOps Engineer"]
    vecs = engine.encode_batch(texts)
    
    assert isinstance(vecs, np.ndarray)
    assert vecs.shape == (3, 384)
    for i in range(3):
        assert np.isclose(np.linalg.norm(vecs[i]), 1.0, atol=1e-5)

def test_empty_or_whitespace_input():
    engine = EmbeddingEngine()
    vec = engine.encode_text("")
    assert vec.shape == (384,)
    assert np.all(vec == 0.0)

def test_embedding_caching():
    engine = EmbeddingEngine()
    text = "Unique caching test text"
    
    # First encode (cache miss)
    hits_before = engine.telemetry["cache_hits"]
    vec1 = engine.encode_text(text)
    
    # Second encode (cache hit)
    vec2 = engine.encode_text(text)
    hits_after = engine.telemetry["cache_hits"]
    
    assert hits_after == hits_before + 1
    assert np.allclose(vec1, vec2)
