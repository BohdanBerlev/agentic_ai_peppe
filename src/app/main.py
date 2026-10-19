from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg

from src.app.db import database_health
from src.app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")

# Pydantic-Modell für ein Work Item (unser Daten-Bauplan)
class WorkItemCreate(BaseModel):
    title: str
    description: Optional[str] = None

class WorkItemUpdate(BaseModel):
    status: str

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
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database unavailable: {exc}") from exc


# --- NEU: Work Item Endpunkte für den Dry Run ---

@app.post("/work-items", status_code=201)
def create_work_item(item: WorkItemCreate):
    """Erstellt ein neues Work Item in PostgreSQL."""
    try:
        with psycopg.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO work_items (title, description) VALUES (%s, %s) RETURNING id, title, description, status, created_at",
                    (item.title, item.description)
                )
                row = cur.fetchone()
                return {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "status": row[3],
                    "created_at": row[4]
                }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")


@app.get("/work-items")
def list_work_items():
    """Listet alle Work Items aus PostgreSQL auf."""
    try:
        with psycopg.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, description, status, created_at FROM work_items ORDER BY id DESC")
                rows = cur.fetchall()
                result = []
                for row in rows:
                    result.append({
                        "id": row[0],
                        "title": row[1],
                        "description": row[2],
                        "status": row[3],
                        "created_at": row[4]
                    })
                return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")


@app.patch("/work-items/{item_id}")
def update_work_item(item_id: int, item: WorkItemUpdate):
    """Aktualisiert den Status eines Work Items (z.B. auf 'done')."""
    try:
        with psycopg.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE work_items SET status = %s WHERE id = %s RETURNING id, title, description, status",
                    (item.status, item_id)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Work item not found")
                return {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "status": row[3]
                }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")


@app.delete("/work-items/{item_id}", status_code=200)
def delete_work_item(item_id: int):
    """Löscht ein Work Item aus PostgreSQL."""
    try:
        with psycopg.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM work_items WHERE id = %s RETURNING id", (item_id,))
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Work item not found")
                return {"status": "deleted", "id": row[0]}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")