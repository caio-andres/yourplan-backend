from datetime import datetime

current_datetime = datetime.now().strftime("%Y-%m-%d")

INDEX_PATH = "app/src/genai/rag/faiss/faiss_index.bin"
DOCS_PATH = "app/src/genai/rag/faiss/faiss_docs.npy"