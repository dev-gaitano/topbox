import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from flask import g, jsonify

from app import create_app
from app.utils.decorators import require_auth
from app.utils.jwt_utils import encode_jwt, generate_access_token


class TestRequireAuth(unittest.TestCase):
    def setUp(self):
        self.flask_app = create_app()
        self.flask_app.config["TESTING"] = True
        self.flask_app.config["JWT_SECRET_KEY"] = "test-secret-key-at-least-32-bytes!"

        @self.flask_app.get("/api/protected-test")
        @require_auth
        def protected_route():
            return (
                jsonify(
                    {
                        "success": True,
                        "user_id": g.current_user_id,
                        "email": g.current_user_email,
                    }
                ),
                200,
            )

        self.client = self.flask_app.test_client()
        self.secret = self.flask_app.config["JWT_SECRET_KEY"]
        self.user_id = "123e4567-e89b-12d3-a456-426614174000"
        self.session_id = 1
        self.active_session = {
            "id": self.session_id,
            "user_id": self.user_id,
            "refresh_token_hash": "hashed-refresh-token",
            "created_at": "2026-07-30T00:00:00",
            "expires_at": "2026-08-30T00:00:00",
            "revoked_at": None,
        }

    def test_missing_authorization_header_returns_401(self):
        response = self.client.get("/api/protected-test")

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json["success"])

    def test_invalid_signature_returns_401(self):
        token = generate_access_token(
            user_id=self.user_id,
            email="user@example.com",
            secret_key="wrong-secret-key-at-least-32-bytes!",
            session_id=self.session_id,
            expires_in_minutes=15,
        )

        response = self.client.get(
            "/api/protected-test",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json["success"])

    def test_expired_token_returns_401(self):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": self.user_id,
            "email": "user@example.com",
            "sid": self.session_id,
            "iat": now - timedelta(hours=2),
            "exp": now - timedelta(hours=1),
            "type": "access",
        }
        token = encode_jwt(payload, self.secret)

        response = self.client.get(
            "/api/protected-test",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json["success"])
        self.assertIn("expired", response.json["message"].lower())

    def test_revoked_session_returns_401(self):
        token = generate_access_token(
            user_id=self.user_id,
            email="user@example.com",
            secret_key=self.secret,
            session_id=self.session_id,
            expires_in_minutes=15,
        )
        revoked_session = {
            **self.active_session,
            "revoked_at": "2026-07-31T09:00:00",
        }

        with patch(
            "app.api.auth.repository.find_session_by_id",
            return_value=revoked_session,
        ):
            response = self.client.get(
                "/api/protected-test",
                headers={"Authorization": f"Bearer {token}"},
            )

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json["success"])
        self.assertIn("revoked", response.json["message"].lower())

    def test_valid_token_allows_access(self):
        token = generate_access_token(
            user_id=self.user_id,
            email="user@example.com",
            secret_key=self.secret,
            session_id=self.session_id,
            expires_in_minutes=15,
        )

        with patch(
            "app.api.auth.repository.find_session_by_id",
            return_value=self.active_session,
        ):
            response = self.client.get(
                "/api/protected-test",
                headers={"Authorization": f"Bearer {token}"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])
        self.assertEqual(response.json["user_id"], self.user_id)
        self.assertEqual(response.json["email"], "user@example.com")


if __name__ == "__main__":
    unittest.main()
