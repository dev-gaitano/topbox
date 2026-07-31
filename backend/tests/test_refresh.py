import unittest
from unittest.mock import patch

from app import create_app


class TestRefresh(unittest.TestCase):
    def setUp(self):
        self.flask_app = create_app()
        self.flask_app.config["TESTING"] = True
        self.flask_app.config["JWT_SECRET_KEY"] = "test-secret-key-at-least-32-bytes!"
        self.flask_app.config["ACCESS_TOKEN_EXPIRES_MINUTES"] = 15
        self.flask_app.config["REFRESH_TOKEN_EXPIRES_DAYS"] = 7
        self.client = self.flask_app.test_client()
        self.user_id = "123e4567-e89b-12d3-a456-426614174000"
        self.refresh_token = "valid-refresh-token"
        self.mock_session = {
            "id": 1,
            "user_id": self.user_id,
            "refresh_token_hash": "hashed-refresh-token",
            "created_at": "2026-07-30T00:00:00",
            "expires_at": "2026-08-30T00:00:00",
            "revoked_at": None,
        }
        self.mock_user = {
            "id": self.user_id,
            "username": "testuser",
            "email": "user@example.com",
            "password_hash": "$2b$12$hashedpasswordhere",
            "created_at": "2026-07-30T00:00:00",
        }

    def test_refresh_valid_token_returns_new_access_token(self):
        """
        Test: POST /api/auth/refresh exchanges a valid refresh token
        for a new access token.
        """
        with patch(
            "app.api.auth.repository.find_session_by_refresh_token",
            return_value=self.mock_session,
        ):
            with patch(
                "app.api.auth.repository.find_user_by_id",
                return_value=self.mock_user,
            ):
                with patch(
                    "app.api.auth.repository.revoke_session",
                    return_value={
                        **self.mock_session,
                        "revoked_at": "2026-07-31T12:00:00",
                    },
                ) as mock_revoke:
                    with patch(
                        "app.api.auth.repository.create_session",
                        return_value={"id": 2},
                    ) as mock_create_session:
                        response = self.client.post(
                            "/api/auth/refresh",
                            json={"refresh_token": self.refresh_token},
                        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertTrue(response.json["success"])
        self.assertIn("access_token", response.json["data"])
        self.assertTrue(response.json["data"]["access_token"])
        self.assertIn("refresh_token", response.json["data"])
        self.assertTrue(mock_revoke.called)
        self.assertTrue(mock_create_session.called)

    def test_refresh_invalid_token_returns_401(self):
        """
        Test: refresh with an unknown refresh token returns 401.
        """
        with patch(
            "app.api.auth.repository.find_session_by_refresh_token",
            return_value=None,
        ):
            response = self.client.post(
                "/api/auth/refresh",
                json={"refresh_token": "unknown-refresh-token"},
            )

        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.is_json)
        self.assertFalse(response.json["success"])

    def test_refresh_missing_token_returns_400(self):
        """
        Test: refresh without a refresh token returns 400.
        """
        response = self.client.post("/api/auth/refresh", json={})

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.is_json)
        self.assertFalse(response.json["success"])


if __name__ == "__main__":
    unittest.main()
