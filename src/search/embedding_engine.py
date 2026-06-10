import time
import hashlib
import logging
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingEngine:
    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern instantiation to prevent reloading model weights."""
        if not cls._instance:
            cls._instance = super(EmbeddingEngine, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load model only once
        if self._model is None:
            logger.info(f"Loading Sentence Transformer model '{model_name}' (Singleton)...")
            start_time = time.time()
            self._model = SentenceTransformer(model_name)
            logger.info(f"Model loaded successfully in {time.time() - start_time:.3f}s on CPU.")
            
        self.model_name = model_name
        self.embedding_cache: Dict[str, np.ndarray] = {}
        self.telemetry = {
            "total_encodes": 0,
            "cache_hits": 0,
            "encode_time_accumulated": 0.0
        }

    def _get_text_hash(self, text: str) -> str:
        """Computes SHA-256 hash of text for caching keys."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def _l2_normalize(self, vector: np.ndarray) -> np.ndarray:
        """L2 normalizes a vector or matrix for Cosine similarity equivalence."""
        norm = np.linalg.norm(vector, axis=-1, keepdims=True)
        # Avoid division by zero
        return vector / np.where(norm == 0, 1.0, norm)

    def encode_text(self, text: str) -> np.ndarray:
        """Generates L2-normalized embedding for a single text string (with caching)."""
        if not isinstance(text, str) or not text.strip():
            return np.zeros(384, dtype=np.float32)
            
        text_hash = self._get_text_hash(text)
        
        # Check cache
        if text_hash in self.embedding_cache:
            self.telemetry["cache_hits"] += 1
            return self.embedding_cache[text_hash]
            
        # Encode
        start = time.time()
        self.telemetry["total_encodes"] += 1
        embedding = self._model.encode([text])[0]
        normalized_embedding = self._l2_normalize(embedding).astype(np.float32)
        
        # Save cache
        self.embedding_cache[text_hash] = normalized_embedding
        self.telemetry["encode_time_accumulated"] += time.time() - start
        
        return normalized_embedding

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Generates L2-normalized embeddings for a list of text strings (batch inference)."""
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
            
        start = time.time()
        # Filter and track texts that are not cached
        uncached_texts = []
        uncached_indices = []
        
        results = [None] * len(texts)
        
        for idx, text in enumerate(texts):
            text_hash = self._get_text_hash(text) if isinstance(text, str) else ""
            if text_hash in self.embedding_cache:
                self.telemetry["cache_hits"] += 1
                results[idx] = self.embedding_cache[text_hash]
            else:
                uncached_texts.append(text if isinstance(text, str) else "")
                uncached_indices.append(idx)
                
        if uncached_texts:
            logger.info(f"Running batch encoding on {len(uncached_texts)} uncached documents...")
            self.telemetry["total_encodes"] += len(uncached_texts)
            embeddings = self._model.encode(uncached_texts)
            normalized_embeddings = self._l2_normalize(embeddings).astype(np.float32)
            
            for idx, raw_idx in enumerate(uncached_indices):
                text_hash = self._get_text_hash(uncached_texts[idx])
                self.embedding_cache[text_hash] = normalized_embeddings[idx]
                results[raw_idx] = normalized_embeddings[idx]
                
        self.telemetry["encode_time_accumulated"] += time.time() - start
        return np.array(results, dtype=np.float32)

if __name__ == "__main__":
    engine1 = EmbeddingEngine()
    engine2 = EmbeddingEngine()
    print("Same instance:", engine1 is engine2)
    
    vec = engine1.encode_text("Hello World")
    print("Vector shape:", vec.shape)
    print("L2 Norm:", np.linalg.norm(vec)) # Should be exactly 1.0 (L2 normalized)
