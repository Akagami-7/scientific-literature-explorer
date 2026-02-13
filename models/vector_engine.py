import faiss
import numpy as np
import os
import pickle


class VectorEngine:
    def __init__(self, dimension=768):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.texts = []
        self.sources = []

        # Load existing index if available
        if os.path.exists("data/faiss_index/index.bin"):
            self.load_index()

    def add_documents(self, vectors, texts, source):
        vectors = np.array(vectors).astype("float32")

        self.index.add(vectors)

        for text in texts:
            self.texts.append(text)
            self.sources.append(source)

    def search(self, query_vector, k=3):
        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, k)

        results = []

        for score, idx in zip(distances[0], indices[0]):
            if idx < len(self.texts):
                results.append({
                    "text": self.texts[idx],
                    "score": float(score),
                    "source": self.sources[idx]
                })

        return results

    def save_index(self):
        os.makedirs("data/faiss_index", exist_ok=True)

        faiss.write_index(self.index, "data/faiss_index/index.bin")

        with open("data/faiss_index/meta.pkl", "wb") as f:
            pickle.dump((self.texts, self.sources), f)

    def load_index(self):
        self.index = faiss.read_index("data/faiss_index/index.bin")

        with open("data/faiss_index/meta.pkl", "rb") as f:
            self.texts, self.sources = pickle.load(f)

    def reset(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.texts = []
        self.sources = []
