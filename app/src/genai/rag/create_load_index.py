import os
import faiss

import numpy as np

from src.genai.rag.embedding import embed_files
from src.genai.rag.utils import DOCS_PATH, INDEX_PATH


def load_or_create_index():
    if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "rb") as f:
            documents = np.load(f, allow_pickle=True).tolist()
    else:
        embeddings, documents = embed_files()
        index = create_index(embeddings)
        faiss.write_index(index, INDEX_PATH)
        with open(DOCS_PATH, "wb") as f:
            np.save(f, documents)

    return index, documents


def create_index(embeddings):
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index


if __name__ == "__main__":
    index, documents = load_or_create_index()
