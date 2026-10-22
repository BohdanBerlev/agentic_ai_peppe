from fastapi import FastAPI, HTTPException

from src.app.db import database_health
from src.app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
    }


@app.get("/db/health")
def db_health() -> dict:
    try:
        return database_health()
    except Exception as exc:  # endpoint should report failure without crashing app
        raise HTTPException(status_code=503, detail="database unavailable") from exc
