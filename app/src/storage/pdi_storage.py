import json
import uuid
import os

from datetime import datetime

PDI_STORAGE_PATH = "./storage/pdis"

os.makedirs(PDI_STORAGE_PATH, exist_ok=True)


def save_pdi(pdi_json: dict) -> str:
    pdi_id = str(uuid.uuid4())

    pdi_data = {
        "id": pdi_id,
        "created_at": datetime.now().isoformat(),
        "data": pdi_json,
    }

    file_path = os.path.join(PDI_STORAGE_PATH, f"{pdi_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(pdi_data, f, ensure_ascii=False, indent=2)

    return pdi_id


def get_pdi(pdi_id: str) -> dict:
    file_path = os.path.join(PDI_STORAGE_PATH, f"{pdi_id}.json")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
