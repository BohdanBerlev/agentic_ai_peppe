from contextlib import asynccontextmanager
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import psycopg
from psycopg_pool import ConnectionPool

from src.app.db import database_health
from src.app.settings import get_settings

settings = get_settings()

# Globaler Connection Pool zur Vermeidung von Resource Exhaustion
pool = ConnectionPool(settings.database_url, open=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    yield
    pool.close()

app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

# --- Pydantic Models mit strikter Input-Validierung ---
class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: str

class WorkItemCreate(BaseModel):
    title: str = Field(..., max_length=100, description="Titel des Work Items")
    description: Optional[str] = Field(default=None, max_length=1000)

class WorkItemUpdate(BaseModel):
    status: str = Field(..., max_length=50)


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
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")

# --- Work Item Endpunkte ---

@app.post("/work-items", status_code=201, response_model=WorkItemResponse)
def create_work_item(item: WorkItemCreate):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO work_items (title, description) VALUES (%s, %s) RETURNING id, title, description, status, created_at",
                    (item.title, item.description)
                )
                row = cur.fetchone()
                return {"id": row[0], "title": row[1], "description": row[2], "status": row[3], "created_at": str(row[4])}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error during creation.")

@app.get("/work-items", response_model=List[WorkItemResponse])
def list_work_items():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, description, status, created_at FROM work_items ORDER BY id DESC")
                rows = cur.fetchall()
                return [
                    {"id": r[0], "title": r[1], "description": r[2], "status": r[3], "created_at": str(r[4])}
                    for r in rows
                ]
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error during fetch.")

@app.patch("/work-items/{item_id}", response_model=WorkItemResponse)
def update_work_item(item_id: int, item: WorkItemUpdate):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE work_items SET status = %s WHERE id = %s RETURNING id, title, description, status, created_at",
                    (item.status, item_id)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Work item not found")
                return {"id": row[0], "title": row[1], "description": row[2], "status": row[3], "created_at": str(row[4])}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error during update.")

@app.delete("/work-items/{item_id}", status_code=200)
def delete_work_item(item_id: int):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM work_items WHERE id = %s RETURNING id", (item_id,))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="Work item not found")
                return {"status": "deleted", "id": item_id}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error during deletion.")