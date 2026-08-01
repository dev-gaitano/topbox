from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app import create_app
from app.utils.jwt_utils import generate_access_token

USER_ID = "123e4567-e89b-12d3-a456-426614174000"
SESSION_ID = 1
JWT_SECRET = "test-secret-key-at-least-32-bytes!"


@pytest.fixture
def client():
    """Test client for flask app"""
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    flask_app.config["JWT_SECRET_KEY"] = JWT_SECRET
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers():
    token = generate_access_token(
        user_id=USER_ID,
        email="user@example.com",
        secret_key=JWT_SECRET,
        session_id=SESSION_ID,
        expires_in_minutes=15,
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def active_session():
    return {
        "id": SESSION_ID,
        "user_id": USER_ID,
        "refresh_token_hash": "hashed",
        "created_at": "2026-07-30T00:00:00",
        "expires_at": "2026-08-30T00:00:00",
        "revoked_at": None,
    }


def test_company_data_returns_none(client, auth_headers, active_session):
    """
    Check if correct status code and json is returned when company data is an
    empty dict or a None type
    """
    with patch(
        "app.api.auth.repository.find_session_by_id",
        return_value=active_session,
    ):
        response = client.post("/api/companies", json={}, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"success": False, "message": "No JSON data provided"}


def test_create_company_requires_auth(client):
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
    assert response.status_code == 401


@patch("app.api.companies.repository.db_connection")
def test_insert_company_success(mock_db_conn, client, auth_headers, active_session):
    """
    Check if correct status code and json is returned on company insertion
    success
    """
    mock_conn = mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = (
        1,
        "Test DB Company",
        datetime(2026, 6, 21, 0, 0, 0),
    )
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    with patch(
        "app.api.auth.repository.find_session_by_id",
        return_value=active_session,
    ):
        response = client.post(
            "/api/companies",
            headers=auth_headers,
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

    # First bind value on INSERT should be the authenticated user_id
    insert_args = mock_cursor.execute.call_args[0][1]
    assert insert_args[0] == USER_ID
