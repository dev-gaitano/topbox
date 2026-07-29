from unittest.mock import patch
import pytest
from app import create_app
from app.api.auth.repository import DuplicateUserError
from app.models.user import User


@pytest.fixture
def client():
    """Test client for Flask app."""
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_signup_existing_username_or_email_returns_409(client):
    """
    Test: signup with existing username/email returns a 409 status code
    and clean error payload, not a raw DB error.
    """
    payload = {
        "username": "existinguser",
        "email": "existing@example.com",
        "password": "ValidPassword123!",
        "confirmed_password": "ValidPassword123!",
    }
    with patch(
        "app.api.auth.repository.signup",
        side_effect=DuplicateUserError(
            "User with given username or email already exists"
        ),
    ):
        response = client.post("/api/auth/signup", json=payload)

    assert response.status_code == 409
    assert response.is_json
    assert "message" in response.json or "error" in response.json


def test_signup_password_under_minimum_length_returns_400(client):
    """
    Test: signup with a password under the minimum rule returns a 400.
    """
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "short",
        "confirmed_password": "short",
    }
    response = client.post("/api/auth/signup", json=payload)

    assert response.status_code == 400
    assert response.is_json
    assert "message" in response.json or "error" in response.json


def test_signup_password_mismatch_returns_400(client):
    """
    Test: signup when password doesn't match confirmed password returns 400 status code.
    """
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "ValidPassword123!",
        "confirmed_password": "MismatchedPassword123!",
    }
    response = client.post("/api/auth/signup", json=payload)

    assert response.status_code == 400
    assert response.is_json
    assert "message" in response.json or "error" in response.json


def test_signup_success_hashes_password_and_returns_201(client):
    """
    Test: successful signup hashes password using bcrypt and returns 201.
    """
    payload = {
        "username": "validuser",
        "email": "valid@example.com",
        "password": "ValidPassword123!",
        "confirmed_password": "ValidPassword123!",
    }
    mock_db_user = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "username": "validuser",
        "email": "valid@example.com",
        "created_at": "2026-07-28T12:00:00",
    }
    with patch(
        "app.api.auth.repository.signup", return_value=mock_db_user
    ) as mock_signup:
        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 201
        assert response.is_json
        assert response.json["success"] is True

        # Verify password_hash argument passed to repository starts with $2b$ (bcrypt hash prefix)
        _, kwargs = mock_signup.call_args
        assert kwargs["username"] == "validuser"
        assert kwargs["email"] == "valid@example.com"
        assert kwargs["password_hash"].startswith("$2b$")


def test_user_handle_signup_data():
    """
    Test: User.handle_signup_data extracts signup payload fields correctly.
    """
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecretPassword123!",
        "confirm_password": "SecretPassword123!",
    }
    username, email, password, confirmed = User.handle_signup_data(data)
    assert username == "testuser"
    assert email == "test@example.com"
    assert password == "SecretPassword123!"
    assert confirmed == "SecretPassword123!"
