from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Optional


class Embedder:
    """
    Wrapper class for SentenceTransformer model to generate text embeddings.
    Loads the model once and reuses it for efficiency.
    """

    def __init__(self):
        # The model is loaded only once when the class is initialized.
        # 'all-MiniLM-L6-v2' is chosen for its speed and efficiency (384 dimensions).
        print("⏳ Loading embedding model: all-MiniLM-L6-v2 (384 dimensions)...")

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model ready.")

    def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Converts an input string into a high-dimensional vector (embedding).

        Args:
            text (str): The text content to be vectorized.

        Returns:
            List[float]: A list of floating point numbers representing the semantic meaning.
            None: If the input text is empty.
        """
        if not text:
            return None

        # 1. Encode text to vector
        # convert_to_numpy=True ensures we get a raw numerical array
        embeddings_numpy = self.model.encode(text, convert_to_numpy=True)

        # 2. Convert NumPy array to standard Python List
        # This is crucial because SQLAlchemy/PostgreSQL expects a standard List, not a NumPy object.
        return embeddings_numpy.tolist()


# Singleton Instance
# We create a global instance to avoid reloading the heavy AI model for every request.
global_embedder = Embedder()