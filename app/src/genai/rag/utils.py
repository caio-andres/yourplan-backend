from datetime import datetime

current_datetime = datetime.now().strftime("%Y-%m-%d")

INDEX_PATH = "./src/genai/rag/faiss/faiss_index.bin"
DOCS_PATH = "./src/genai/rag/faiss/faiss_docs.npy"