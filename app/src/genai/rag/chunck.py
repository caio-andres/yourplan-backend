from pandas import DataFrame

from src.genai.agent.config import client


def chunk_dataframe(df: DataFrame, max_size_per_chunk=100):
    df = df.astype(str)
    return [
        df.iloc[i : i + max_size_per_chunk]
        for i in range(0, len(df), max_size_per_chunk)
    ]


def process_chunk(data: DataFrame):
    documents = [" ".join(row) for row in data.values]
    emb = client.models.embed_content(model="gemini-embedding-001", contents=documents)
    # Correção: acessar .embedding de cada item
    return [e.embedding for e in emb.embeddings], documents
