from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_company_data(client):
    response = client.post("/api/companies", json={})

    assert response.status_code == 400
    assert response.json == {"success": False, "message": "No JSON data provided"}


@patch("main.db_connection")
def test_insert_company_db_returns_none(mock_db_conn, client):
    mock_conn = mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = ()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.post(
        "/api/companies",
        json={
            "businessName": "Test DB Company",
            "logo": "test.png",
            "industry": "Testing",
            "email": "test@db.com",
            "description": "Verify DB insertion",
            "targetAudience": "Developers",
            "tone": "Formal",
        },
    )

    assert response.status_code == 500
    assert response.json == {
        "success": False,
        "message": "Failed to return created company data",
    }


@patch("main.db_connection")
def test_insert_company_success(mock_db_conn, client):
    mock_conn = mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = (
        1,
        "Test DB Company",
        datetime(2026, 6, 21, 0, 0, 0),
    )
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.post(
        "/api/companies",
        json={
            "businessName": "Test DB Company",
            "logo": "test.png",
            "industry": "Testing",
            "email": "test@db.com",
            "description": "Verify DB insertion",
            "targetAudience": "Developers",
            "tone": "Formal",
        },
    )

    assert response.status_code == 201
    assert response.json == {
        "success": True,
        "message": "Company created successfully",
        "data": {
            "id": 1,
            "name": "Test DB Company",
            "created_at": "2026-06-21T00:00:00",
        },
    }
