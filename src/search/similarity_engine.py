import os
import sys
import logging
import numpy as np
from typing import Dict

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.search.embedding_engine import EmbeddingEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarityEngine:
    def __init__(self, embedding_engine: EmbeddingEngine = None):
        self.embedding_engine = embedding_engine or EmbeddingEngine()

    def compute_similarity(self, text_a: str, text_b: str) -> Dict[str, float]:
        """Computes Cosine Similarity between two text strings.
        
        Loads embeddings, performs inner product, and clamps output to [0.0, 1.0].
        """
        if not isinstance(text_a, str) or not isinstance(text_b, str):
            return {"similarity": 0.0}
            
        if not text_a.strip() or not text_b.strip():
            return {"similarity": 0.0}
            
        # 1. Generate L2-normalized embeddings
        embedding_a = self.embedding_engine.encode_text(text_a)
        embedding_b = self.embedding_engine.encode_text(text_b)
        
        # 2. Cosine similarity of L2 normalized vectors is exactly their dot product
        similarity = float(np.dot(embedding_a, embedding_b))
        
        # 3. Clip to [0.0, 1.0] range
        similarity = max(0.0, min(1.0, similarity))
        
        return {
            "similarity": round(similarity, 4)
        }

if __name__ == "__main__":
    engine = SimilarityEngine()
    res = engine.compute_similarity(
        "Machine Learning Engineer specializing in deep learning",
        "AI Engineer training PyTorch models"
    )
    print("Similarity:", res)
