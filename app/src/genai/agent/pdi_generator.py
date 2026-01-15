from datetime import datetime
from google.genai import types

from src.genai.rag.search_index import search
from src.genai.rag.create_load_index import load_or_create_index
from src.genai.agent.config import client
from src.genai.prompt.pdi_generator import SYSTEM_PROMPT_PDI_GENERATOR_AGENT


class PDIGeneratorAI:
    def __init__(self, user_prompt: str):
        self.user_prompt = user_prompt
        self.system_prompt = SYSTEM_PROMPT_PDI_GENERATOR_AGENT

    def _get_json_structure_from_rag(self):
        """Busca a estrutura JSON do RAG"""
        try:
            index, documents = load_or_create_index()
            relevant_docs = search("estrutura JSON PDI schema", index, documents, k=1)

            if relevant_docs:
                return relevant_docs[0][0]  # Retorna o primeiro documento
            return "{}"
        except Exception as e:
            print(f"Erro ao buscar estrutura JSON do RAG: {e}")
            return "{}"

    def answer(self):
        json_structure = self._get_json_structure_from_rag()

        current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt.format(
                    json_structure=json_structure, CURRENT_DATETIME=current_datetime
                )
            ),
            contents=self.user_prompt,
        )
        
        print(response.text)
        return response.text
