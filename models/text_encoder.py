from sentence_transformers import SentenceTransformer
import numpy as np
import torch


class TextEncoder:
    _instance = None
    _model = None

    def __new__(cls, model_name="all-mpnet-base-v2"):
        if cls._instance is None:
            cls._instance = super(TextEncoder, cls).__new__(cls)

            print("Loading Embedding Model (MiniLM)...")

            device = "cuda" if torch.cuda.is_available() else "cpu"

            cls._model = SentenceTransformer(model_name, device=device)

        return cls._instance

    def encode(self, texts, normalize=True):
        """
        Convert text(s) to embeddings.
        
        Parameters:
            texts (str or list[str])
            normalize (bool): L2 normalize embeddings (recommended for cosine similarity)

        Returns:
            np.ndarray
        """

        # Allow single string input
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self._model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True
        )

        if normalize:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / (norms + 1e-10)

        return embeddings
