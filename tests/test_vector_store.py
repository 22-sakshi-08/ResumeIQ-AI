import sys
import os
import numpy as np
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search.vector_store import VectorStore

def test_vector_store_build_and_search():
    store = VectorStore(dimension=3)
    
    # Define simple orthogonal vectors
    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ], dtype=np.float32)
    
    metadata = [
        {"id": "doc_x"},
        {"id": "doc_y"},
        {"id": "doc_z"}
    ]
    
    store.build_index(embeddings, metadata)
    assert store.index.ntotal == 3
    
    # Query matching doc_x exactly
    query = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    results = store.search(query, top_k=2)
    
    assert len(results) == 2
    assert results[0][0]["id"] == "doc_x"
    assert np.isclose(results[0][1], 1.0, atol=1e-5)
    assert results[1][1] < 0.5

def test_vector_store_save_load(tmp_path):
    store = VectorStore(dimension=3)
    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ], dtype=np.float32)
    metadata = [{"id": "x"}, {"id": "y"}]
    
    store.build_index(embeddings, metadata)
    
    # Save
    save_prefix = str(tmp_path / "test_index")
    store.save(save_prefix)
    
    # Assert files exist
    assert os.path.exists(save_prefix + ".index")
    assert os.path.exists(save_prefix + ".meta")
    
    # Load into a new store
    new_store = VectorStore(dimension=3)
    new_store.load(save_prefix)
    
    assert new_store.index.ntotal == 2
    assert new_store.metadata[0]["id"] == "x"
    assert new_store.metadata[1]["id"] == "y"
