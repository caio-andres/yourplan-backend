import pandas as pd

import os
import json

from src.genai.agent.config import client
from src.genai.rag.chunck import chunk_dataframe, process_chunk


def embed_files():
    base_path = "app/src/genai/rag/knowledge_source/"
    file_names = [
        f
        for f in os.listdir(base_path)
        if os.path.isfile(os.path.join(base_path, f))
        and f.lower().endswith((".txt", ".csv", ".json"))
    ]

    embeddings_list = []
    documents_list = []

    for file in file_names:
        file_path = os.path.join(base_path, file)

        if file.lower().endswith(".csv"):
            df = pd.read_csv(file_path)
            chunks = chunk_dataframe(df)
            for chunk in chunks:
                embeddings, documents = process_chunk(chunk)
                embeddings_list.extend(embeddings)
                documents_list.extend(documents)

        elif file.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            emb_data = client.models.embed_content(
                model="gemini-embedding-001", contents=content
            )
            # Correção: acessar .embeddings[0].values
            embeddings_list.append(emb_data.embeddings[0].values)
            documents_list.append(content)

        elif file.lower().endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            content = json.dumps(data, ensure_ascii=False, indent=2)

            emb = client.models.embed_content(
                model="gemini-embedding-001", contents=content
            )

            # Correção: acessar .embeddings[0].values
            embeddings_list.append(emb.embeddings[0].values)
            documents_list.append(content)

    return embeddings_list, documents_list
