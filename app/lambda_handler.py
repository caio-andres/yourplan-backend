from src.genai.rag.rag import search, load_or_create_index
from src.genai.agent.pdi_generator import PDIGeneratorAI

def lambda_function(context, event):
  user_prompt = context.user_prompt
  index, documents = load_or_create_index()
  results = search(user_prompt, index, documents, k=3)
  
  
  