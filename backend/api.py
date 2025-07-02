"""API endpoints for the AI-Driven Testing project."""
import os
import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from llm_manager import LLMManager
from schemas import PromptData, ResponseData
from export_manager import ExportManager
from module_manager import ModuleManager

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
module_manager = ModuleManager()

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
    """Return the list of allowed models and container status."""
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
    """Process a prompt request and return the LLM response."""
    try:
        print("📥 Request received:")
        print(req)

        model_id = req.model.id

        if model_id not in manager.active_models:
            await run_in_threadpool(manager.start_model_container, model_id)

        response_data: ResponseData = await run_in_threadpool(
            manager.send_prompt, req
        )

        # Process code coverage if requested and source code is provided
        if hasattr(req.input, 'enable_code_coverage') and req.input.enable_code_coverage:
            if req.input.source_code and response_data.output.code:
                try:
                    # Run code coverage analysis on generated tests
                    coverage_analyzer = module_manager.get_module("code_coverage")
                    if coverage_analyzer:
                        coverage_result = await run_in_threadpool(
                            coverage_analyzer.analyze_coverage,
                            req.input.source_code,
                            response_data.output.code
                        )
                        response_data.output.code_coverage = coverage_result
                except Exception as cov_exc:
                    print(f"⚠️ Code coverage analysis failed: {cov_exc}")
                    # Don't fail the entire request, just log the error
                    response_data.output.code_coverage = {
                        "error": str(cov_exc),
                        "status": "failed"
                    }

        return {
            "response_markdown": response_data.output.markdown,
            "total_seconds": response_data.timing.generation_time,
            "code_coverage": response_data.output.code_coverage,
        }

    except Exception as exc:
        import traceback

        traceback.print_exc()  # ⬅️ Add this
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/shutdown")
async def shutdown(req: Dict[str, str]):
    """Shutdown a running model container."""
    model_id = req.get("model_id")
    if not model_id:
        raise HTTPException(status_code=400, detail="Missing 'model_id'")
    await run_in_threadpool(manager.stop_model_container, model_id)
    return {"status": "stopped", "model_id": model_id}


# --------------------------------------------------------------------------- #
# Export endpoints
# --------------------------------------------------------------------------- #
@app.get("/export/formats")
async def get_export_formats():
    """Return list of supported export formats."""
    export_manager = ExportManager()
    return {"formats": export_manager.get_supported_formats()}


@app.post("/export")
async def export_content(req: Dict):
    """
    Export content in specified format(s).

    Expected request body:
    {
        "content": "Content to export",
        "format": "json|markdown|http|txt|xml",
        "filename": "optional_filename",
        "export_all": false
    }
    """
    try:
        content = req.get("content")
        export_format = req.get("format", "markdown")
        filename = req.get("filename")
        export_all = req.get("export_all", False)

        if not content:
            raise HTTPException(
                status_code=400, detail="Missing 'content' field"
            )

        export_manager = ExportManager()

        if export_all:
            # Export in all formats
            export_files = export_manager.export_all_formats(
                content, base_filename=filename or "api_export"
            )
            return {
                "status": "success",
                "message": "Exported in all formats",
                "files": export_files,
            }
        else:
            # Export in specified format
            if export_format not in export_manager.get_supported_formats():
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported format: {export_format}",
                )

            export_filename = filename or f"api_export.{export_format}"
            if export_format == "json" and not export_filename.endswith(
                "_formatted.json"
            ):
                export_filename = export_filename.replace(
                    ".json", "_formatted.json"
                )

            export_path = export_manager.export_content(
                content, export_format, export_filename
            )

            return {
                "status": "success",
                "message": f"Exported in {export_format} format",
                "file": export_path,
            }

    except Exception as exc:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
