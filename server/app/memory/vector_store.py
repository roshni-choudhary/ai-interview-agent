import numpy as np
import os
import json
from typing import List, Dict, Any, Tuple

class SimpleEmbedder:
    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def embed(self, text: str) -> np.ndarray:
        # High quality hash-based lightweight embedder
        vector = np.zeros(self.dimension)
        words = text.lower().split()
        if not words:
            return vector
            
        for i, word in enumerate(words):
            # Compute a stable hash of the word
            h = hash(word) % self.dimension
            # Apply TF-IDF-like weight based on position/length
            weight = 1.0 / (1.0 + 0.1 * i)
            vector[h] += weight * len(word)
            
        # Normalize vector
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector

class VectorMemory:
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.embedder = SimpleEmbedder(dimension)
        self.vectors: List[np.ndarray] = []
        self.documents: List[Dict[str, Any]] = []

    def add(self, text: str, metadata: Dict[str, Any] = None) -> int:
        vector = self.embedder.embed(text)
        self.vectors.append(vector)
        idx = len(self.documents)
        self.documents.append({
            "id": idx,
            "text": text,
            "metadata": metadata or {}
        })
        return idx

    def search(self, query: str, k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        if not self.vectors:
            return []
            
        q_vec = self.embedder.embed(query)
        scores = []
        
        for idx, vec in enumerate(self.vectors):
            # Cosine similarity since both are normalized
            sim = float(np.dot(q_vec, vec))
            scores.append((self.documents[idx], sim))
            
        # Sort descending by similarity
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]

    def save(self, filepath: str):
        data = {
            "dimension": self.dimension,
            "vectors": [v.tolist() for v in self.vectors],
            "documents": self.documents
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load(self, filepath: str):
        if not os.path.exists(filepath):
            return
        with open(filepath, "r") as f:
            data = json.load(f)
            
        self.dimension = data["dimension"]
        self.vectors = [np.array(v) for v in data["vectors"]]
        self.documents = data["documents"]

class SessionMemory:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.store = VectorMemory()
        self.db_path = f"memory_user_{user_id}.json"
        
        # Load existing if available
        if os.path.exists(self.db_path):
            self.store.load(self.db_path)

    def record_session_event(self, event_type: str, details: str, metadata: Dict[str, Any] = None):
        meta = metadata or {}
        meta["event_type"] = event_type
        self.store.add(details, meta)
        self.store.save(self.db_path)

    def recall_insights(self, context_query: str, limit: int = 3) -> List[Dict[str, Any]]:
        results = self.store.search(context_query, k=limit)
        return [item[0] for item in results]
