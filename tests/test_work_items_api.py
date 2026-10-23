import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_health_endpoints():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


@patch("src.app.main.pool")
def test_create_work_item(mock_pool):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        1, "Setup Pipeline", "Initial LangGraph Pipeline", "open", "2026-10-19T10:00:00"
    )
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_pool.connection.return_value.__enter__.return_value = mock_conn

    res = client.post("/work-items", json={"title": "Setup Pipeline", "description": "Initial LangGraph Pipeline"})
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == 1
    assert data["title"] == "Setup Pipeline"
    assert data["status"] == "open"


@patch("src.app.main.pool")
def test_list_work_items(mock_pool):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, "Task 1", "Desc 1", "open", "2026-10-19T10:00:00"),
        (2, "Task 2", "Desc 2", "done", "2026-10-19T11:00:00"),
    ]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_pool.connection.return_value.__enter__.return_value = mock_conn

    res = client.get("/work-items")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 2
    assert items[0]["id"] == 1
    assert items[1]["status"] == "done"


@patch("src.app.main.pool")
def test_update_work_item_status(mock_pool):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "Task 1", "Desc 1", "done", "2026-10-19T12:00:00")
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_pool.connection.return_value.__enter__.return_value = mock_conn

    res = client.patch("/work-items/1", json={"status": "done"})
    assert res.status_code == 200
    assert res.json()["status"] == "done"


@patch("src.app.main.pool")
def test_delete_work_item(mock_pool):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_pool.connection.return_value.__enter__.return_value = mock_conn

    res = client.delete("/work-items/1")
    assert res.status_code == 200
    assert res.json()["status"] == "deleted"


def test_work_items_real_postgres_lifecycle():
    """Real PostgreSQL CRUD lifecycle test (#6): verifies actual DB persistence when PostgreSQL is reachable."""
    import os
    import psycopg
    from src.app.settings import get_settings

    settings = get_settings()
    try:
        with psycopg.connect(settings.database_url, connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS work_items (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        status VARCHAR(50) DEFAULT 'open',
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )
            conn.commit()
    except Exception as exc:
        if os.getenv("STARTER_DATABASE_TEST") == "1":
            pytest.fail(f"PostgreSQL must be reachable in CI, but connection failed: {exc}")
        pytest.skip(f"Local PostgreSQL not running ({exc}); skipping live DB lifecycle test.")

    with TestClient(app) as live_client:
        # 1. CREATE
        create_res = live_client.post(
            "/work-items",
            json={"title": "Real DB Persistence Check", "description": "End-to-end PostgreSQL lifecycle"},
        )
        assert create_res.status_code == 201
        created = create_res.json()
        item_id = created["id"]
        assert created["status"] == "open"

        # 2. READ / LIST
        list_res = live_client.get("/work-items")
        assert list_res.status_code == 200
        assert any(i["id"] == item_id and i["title"] == "Real DB Persistence Check" for i in list_res.json())

        # 3. UPDATE (PATCH)
        patch_res = live_client.patch(f"/work-items/{item_id}", json={"status": "in_progress"})
        assert patch_res.status_code == 200
        assert patch_res.json()["status"] == "in_progress"

        # 4. DELETE
        del_res = live_client.delete(f"/work-items/{item_id}")
        assert del_res.status_code == 200
        assert del_res.json() == {"status": "deleted", "id": item_id}

        # 5. VERIFY DELETION (404 on second delete)
        del_again = live_client.delete(f"/work-items/{item_id}")
        assert del_again.status_code == 404
