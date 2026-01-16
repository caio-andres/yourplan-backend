import json
import sys
import re

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask, request, jsonify
from src.genai.agent.pdi_generator import PDIGeneratorAI
from src.response.format import response_format

app = Flask(__name__)


@app.route("/api/health")
def health_check():
    return response_format(200, {"status": "ok"})


@app.route("/api/pdi/<int:pdi_id>", methods=["GET"])
def show_pdi(pdi_id: int):
    return response_format(200, {"pdi": {"id": pdi_id}})


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
            return response_format(200, pdi_json)
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
