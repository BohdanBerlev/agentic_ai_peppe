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
