import os
import json
import logging
import pickle
import numpy as np
import faiss
from typing import List, Dict, Tuple, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        # Flat Inner Product index: Cosine similarity equivalent on L2 normalized vectors
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata: List[Dict[str, Any]] = []

    def build_index(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """Builds a new FAISS index from scratch using embeddings and matching metadata."""
        if len(embeddings) != len(metadata):
            raise ValueError(f"Embeddings count ({len(embeddings)}) must match metadata count ({len(metadata)}).")
            
        # Clear existing
        self.index = faiss.IndexFlatIP(self.dimension)
        self.metadata = []
        
        if len(embeddings) == 0:
            return
            
        # Embeddings must be float32 for FAISS
        embeddings_f32 = embeddings.astype(np.float32)
        
        # Add to index
        self.index.add(embeddings_f32)
        self.metadata = list(metadata)
        logger.info(f"Built FAISS index with {self.index.ntotal} vectors.")

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Queries the index and returns matching metadata along with cosine similarity scores."""
        if self.index.ntotal == 0:
            return []
            
        # Ensure 2D shape for FAISS search
        if len(query_embedding.shape) == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
            
        query_embedding_f32 = query_embedding.astype(np.float32)
        
        # Cap top_k to ntotal
        top_k = min(top_k, self.index.ntotal)
        if top_k == 0:
            return []
            
        # Search index
        scores, indices = self.index.search(query_embedding_f32, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            # Score represents Inner Product (Cosine similarity on normalized inputs)
            results.append((self.metadata[idx], float(score)))
            
        return results

    def save(self, filepath: str):
        """Serializes the FAISS index and metadata dictionary to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save FAISS index
        faiss_path = filepath + ".index"
        faiss.write_index(self.index, faiss_path)
        
        # Save metadata and config mapper
        meta_path = filepath + ".meta"
        with open(meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)
            
        logger.info(f"FAISS Index saved successfully to {faiss_path} and metadata to {meta_path}")

    def load(self, filepath: str):
        """Loads index and metadata mapper from disk."""
        faiss_path = filepath + ".index"
        meta_path = filepath + ".meta"
        
        if not os.path.exists(faiss_path) or not os.path.exists(meta_path):
            raise FileNotFoundError(f"FAISS index components not found under prefix: {filepath}")
            
        # Load FAISS index
        self.index = faiss.read_index(faiss_path)
        
        # Load metadata
        with open(meta_path, 'rb') as f:
            self.metadata = pickle.load(f)
            
        logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors from {filepath}")
        return self

if __name__ == "__main__":
    store = VectorStore()
    
    # 2 dummy embeddings
    embeds = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ], dtype=np.float32)
    # L2 normalize
    embeds = embeds / np.linalg.norm(embeds, axis=-1, keepdims=True)
    
    metadata = [{"id": "doc_1"}, {"id": "doc_2"}]
    store = VectorStore(dimension=3)
    store.build_index(embeds, metadata)
    
    query = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    res = store.search(query, top_k=2)
    print("Search Results:", res)
