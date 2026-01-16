import json
import sys
import re

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.genai.agent.pdi_generator import PDIGeneratorAI
from src.response.format import response_format
from src.storage.pdi_storage import save_pdi, get_pdi

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/health")
def health_check():
    return response_format(200, {"status": "ok"})


@app.route("/api/pdi", methods=["POST"])
def send_pdi_payload():
    try:
        data = request.get_json()

        if not data or "user_prompt" not in data:
            return response_format(400, {"error": "Campo 'user_prompt' é obrigatório."})

        user_prompt = data["user_prompt"]

        agent = PDIGeneratorAI(user_prompt=user_prompt)
        pdi_response = agent.answer()

        # Limpa a resposta: remove ```json, ``` e espaços extras
        pdi_response = re.sub(r"```json\s*", "", pdi_response)
        pdi_response = re.sub(r"```\s*$", "", pdi_response)
        pdi_response = pdi_response.strip()

        try:
            pdi_json = json.loads(pdi_response)
            pdi_id = save_pdi(pdi_json)

            return response_format(200, {"pdi_id": pdi_id, "pdi": pdi_json})

        except json.JSONDecodeError as e:
            return response_format(
                500,
                {
                    "error": "Erro ao parsear JSON",
                    "details": str(e),
                    "raw_response": pdi_response,
                },
            )

    except Exception as e:
        return response_format(500, {"error": str(e)})


@app.route("/api/pdi/<pdi_id>", methods=["GET"])
def get_pdi_by_id(pdi_id):
    try:
        pdi = get_pdi(pdi_id)

        if not pdi:
            return response_format(404, {"error": "PDI não encontrado."})

        return response_format(200, pdi)
    except Exception as e:
        return response_format(500, {"error": str(e)})
