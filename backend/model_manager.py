import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_MODELS = "allowed_models.json"


def load_models():
    """Load allowed models from configuration."""
    config_path = os.path.join(SCRIPT_DIR, ALLOWED_MODELS)
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("models", [])
