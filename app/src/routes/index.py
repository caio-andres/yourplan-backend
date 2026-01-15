import json
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask, request, jsonify
from src.genai.agent.pdi_generator import PDIGeneratorAI

app = Flask(__name__)


@app.route("/api/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/api/pdi/<int:pdi_id>", methods=["GET"])
def show_pdi(pdi_id: int):
    return jsonify({"pdi": {"id": pdi_id}}), 200


@app.route("/api/pdi", methods=["POST"])
def send_pdi_payload():
    data = request.get_json()

    if not data or "user_prompt" not in data:
        return jsonify({"error": "Campo 'user_prompt' é obrigatório."}), 400

    user_prompt = data["user_prompt"]

    agent = PDIGeneratorAI(user_prompt=user_prompt)
    pdi_response = agent.answer()

    try:
        pdi_json = json.loads(pdi_response)
        return jsonify(pdi_json), 200
    except json.JSONDecodeError:
        return jsonify({"raw_response": pdi_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
