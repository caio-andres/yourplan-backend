import numpy as np

from src.genai.agent.config import client


def search(query, index, documents, k=1):
    query_embedding = (
        np.array(
            client.models.embed_content(model="gemini-embedding-001", contents=query)
            .embeddings[0]
            .values
        )
        .reshape(1, -1)
        .astype("float32")
    )

    D, I = index.search(query_embedding, k)
    return [(documents[i], D[0][idx]) for idx, i in enumerate(I[0])]
