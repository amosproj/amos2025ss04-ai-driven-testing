"""API endpoints for the AI-Driven Testing project."""
"""API endpoints for the AI-Driven Testing project."""
import os
import json
import importlib
import inspect
import logging
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
# Helper functions for modules
# --------------------------------------------------------------------------- #
def discover_modules() -> List[Dict[str, str]]:
    """Automatically discover all valid modules in the modules directory.

    Returns a list of module information dictionaries.
    """
    modules_dir = os.path.join(SCRIPT_DIR, "modules")
    available_modules = []

    # Get all Python files in the modules directory
    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and filename not in [
            "__init__.py",
            "base.py",
        ]:
            module_name = filename[:-3]  # Remove .py extension

            try:
                # Convert snake_case to CamelCase for class name
                class_name = "".join(
                    word.capitalize() for word in module_name.split("_")
                )

                # Import the module dynamically
                module = importlib.import_module(f"modules.{module_name}")

                # Check if the class exists and has the required methods
                if hasattr(module, class_name):
                    cls = getattr(module, class_name)
                    if (
                        inspect.isclass(cls)
                        and hasattr(cls, "applies_before")
                        and hasattr(cls, "applies_after")
                    ):
                        try:
                            # Try to instantiate to check if it's valid
                            instance = cls()

                            available_modules.append(
                                {
                                    "id": module_name,
                                    "name": class_name,
                                    "filename": filename,
                                    "applies_before": (
                                        instance.applies_before()
                                        if callable(instance.applies_before)
                                        else False
                                    ),
                                    "applies_after": (
                                        instance.applies_after()
                                        if callable(instance.applies_after)
                                        else False
                                    ),
                                    "description": cls.__doc__
                                    or f"Module: {class_name}",
                                    "dependencies": (
                                        instance.dependencies_names() or []
                                    ),
                                }
                            )
                        except Exception as e:
                            print(
                                f"Warning: Could not instantiate module {module_name}: {e}"
                            )
                            continue

            except Exception as e:
                # Skip modules that can't be imported or instantiated
                print(f"Warning: Could not load module {module_name}: {e}")
                continue

    return available_modules


async def process_prompt_request(req: PromptData) -> Dict:
    """Process a prompt request through the LLM pipeline with optional module processing."""
    logger.debug(f"Request details: {req}")

    model_id = req.model.id

    # Validate model
    if not any(m["id"] == model_id for m in AVAILABLE_MODELS):
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_id}' is not in the list of allowed models",
        )

    # Load and activate requested modules
    active_modules = []
    if req.modules:
        logger.info(f"Loading modules: {req.modules}")
        active_modules = module_manager.load_modules(req.modules)
        logger.info(f"Loaded {len(active_modules)} modules successfully")

    # Start model container if not running
    if model_id not in manager.active_models:
        logger.info(f"Starting model container for {model_id}")
        await run_in_threadpool(manager.start_model_container, model_id)

    # Apply before modules
    processed_prompt_data = req
    if active_modules:
        logger.info("Applying before modules...")
        processed_prompt_data = await run_in_threadpool(
            module_manager.apply_before_modules, active_modules, req
        )

    # Send prompt to model
    response_data: ResponseData = await run_in_threadpool(
        manager.send_prompt, processed_prompt_data
    )

    # Apply after modules
    if active_modules:
        logger.info("Applying after modules...")
        response_data = await run_in_threadpool(
            module_manager.apply_after_modules,
            active_modules,
            response_data,
            processed_prompt_data,
        )

    return format_prompt_response(
        response_data, processed_prompt_data, req.modules or []
    )


def format_prompt_response(
    response_data: ResponseData,
    processed_prompt_data: PromptData,
    modules_used: List[str],
) -> Dict:
    """Format the response data into a structured dictionary."""
    return {
        "response_markdown": response_data.output.markdown,
        "total_seconds": response_data.timing.generation_time,
        "modules_used": modules_used,
        "output": {
            "code": response_data.output.code,
            "syntax_valid": response_data.output.syntax_valid,
            "ccc_complexity": response_data.output.ccc_complexity,
            "mcc_complexity": response_data.output.mcc_complexity,
            "lm_eval": response_data.output.lm_eval,
        },
        "timing": {
            "loading_time": response_data.timing.loading_time,
            "generation_time": response_data.timing.generation_time,
        },
        "prompt_data": {
            "token_count": processed_prompt_data.token_count,
            "token_count_estimated": processed_prompt_data.token_count_estimated,
            "ccc_complexity": processed_prompt_data.ccc_complexity,
            "mcc_complexity": processed_prompt_data.mcc_complexity,
            "rag_sources": processed_prompt_data.rag_sources,
        },
    }


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


@app.post("/prompt")
async def prompt(req: PromptData):
    """Process a prompt request through the LLM pipeline with optional module processing."""
    try:
        return await process_prompt_request(req)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


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