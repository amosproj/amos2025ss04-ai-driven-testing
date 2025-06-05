import os
import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from llm_manager import LLMManager
from schemas import PromptData, ResponseData

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_MODELS = "allowed_models.json"

# --------------------------------------------------------------------------- #
# FastAPI initialisation
# --------------------------------------------------------------------------- #
app = FastAPI(
    title="Local-Ollama API",
    description="Tiny FastAPI wrapper around LLMManager; good enough for a UI.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

manager = LLMManager()

# --------------------------------------------------------------------------- #
# Helper – load config once
# --------------------------------------------------------------------------- #
with open(
    os.path.join(SCRIPT_DIR, ALLOWED_MODELS), "r", encoding="utf-8"
) as fh:
    _raw_cfg = json.load(fh)
AVAILABLE_MODELS: List[Dict[str, str]] = _raw_cfg.get("models", [])


# --------------------------------------------------------------------------- #
# End-points
# --------------------------------------------------------------------------- #
@app.get("/models")
def list_models() -> List[Dict]:
    """
    Returns the list of allowed models and whether the container is currently running.
    """
    out = []
    for m in AVAILABLE_MODELS:
        m_id = m["id"]
        out.append(
            {
                "id": m_id,
                "name": m["name"],
                "running": m_id in manager.active_models,
                "licence": m.get("licence", ""),
                "licence_link": m.get("licence_link", ""),
            }
        )
    return out


'''
@app.post("/prompt")
async def prompt(req: PromptData):
    """
    1. Start container for given model (if not running)
    2. Send prompt to model
    3. Return Markdown + timing
    """
    try:
        model_id = req.model.id

        if model_id not in manager.active_models:
            await run_in_threadpool(manager.start_model_container, model_id)

        response_data: ResponseData = await run_in_threadpool(
            manager.send_prompt, req
        )

        return {
            "response_markdown": response_data.output.markdown,
            "total_seconds": response_data.timing.generation_time,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

'''


@app.post("/prompt")
async def prompt(req: PromptData):
    try:
        print("📥 Request received:")
        print(req)

        model_id = req.model.id

        if model_id not in manager.active_models:
            await run_in_threadpool(manager.start_model_container, model_id)

        response_data: ResponseData = await run_in_threadpool(
            manager.send_prompt, req
        )

        return {
            "response_markdown": response_data.output.markdown,
            "total_seconds": response_data.timing.generation_time,
        }

    except Exception as exc:
        import traceback

        traceback.print_exc()  # ⬅️ Add this
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/shutdown")
async def shutdown(req: Dict[str, str]):
    """
    Shutdown a running model container.
    """
    model_id = req.get("model_id")
    if not model_id:
        raise HTTPException(status_code=400, detail="Missing 'model_id'")
    await run_in_threadpool(manager.stop_model_container, model_id)
    return {"status": "stopped", "model_id": model_id}
