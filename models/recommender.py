import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
    def __init__(self):
        """
        Simple in-memory paper store.
        Each item:
        {
            "title": str,
            "embedding": np.array
        }
        """
        self.paper_store = []

    def add_paper(self, title, embedding):
        """
        Store paper embedding for recommendation.
        """
        self.paper_store.append({
            "title": title,
            "embedding": embedding
        })

    def get_recommendations(self, query_embedding, top_k=3):
        """
        Returns top_k similar papers based on cosine similarity.
        """
        if not self.paper_store:
            return []

        embeddings = np.array([p["embedding"] for p in self.paper_store])
        titles = [p["title"] for p in self.paper_store]

        # Compute similarity
        similarities = cosine_similarity(
            [query_embedding], embeddings
        )[0]

        # Sort by similarity
        ranked_indices = np.argsort(similarities)[::-1]

        recommendations = []
        for idx in ranked_indices[:top_k]:
            recommendations.append({
                "title": titles[idx],
                "score": float(similarities[idx])
            })

        return recommendations
