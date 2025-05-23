import os
import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from llm_manager import LLMManager

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
    allow_origins=["http://localhost:3000"],
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
# Pydantic request / response models
# --------------------------------------------------------------------------- #
class PromptRequest(BaseModel):
    model_id: str
    prompt: str


class PromptResponse(BaseModel):
    response_markdown: str
    total_seconds: float


class ShutdownRequest(BaseModel):
    model_id: str


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


@app.post("/prompt", response_model=PromptResponse)
async def prompt(req: PromptRequest):
    """
    1. Ensure the container for `model_id` is up (creates it if missing)
    2. Send the prompt
    3. Return result + some metrics
    """
    try:
        # LLMManager is synchronous → run it in a thread so FastAPI stays async-friendly
        if req.model_id not in manager.active_models:
            await run_in_threadpool(
                manager.start_model_container, req.model_id
            )

        response, load_t, total_t = await run_in_threadpool(
            manager.send_prompt, req.model_id, req.prompt
        )

        return PromptResponse(
            response_markdown=response,
            total_seconds=total_t,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/shutdown")
async def shutdown(req: ShutdownRequest):
    """
    Stop & remove a running model container.
    """
    await run_in_threadpool(manager.stop_model_container, req.model_id)
    return {"status": "stopped", "model_id": req.model_id}
