import unittest
from unittest.mock import patch
from app import create_app


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.flask_app = create_app()
        self.flask_app.config["TESTING"] = True
        self.client = self.flask_app.test_client()

    def test_login_wrong_password_returns_401(self):
        """
        Test: login with correct email but wrong password returns 401.
        """
        payload = {
            "email": "user@example.com",
            "password": "wrongpassword123",
        }
        mock_user = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user@example.com",
            "username": "testuser",
            "password_hash": "$2b$12$hashedpasswordhere",
            "created_at": "2026-07-30T00:00:00",
        }
        with patch(
            "app.api.auth.repository.find_user_by_email",
            return_value=mock_user,
        ):
            with patch("app.api.auth.service.check_password", return_value=False):
                response = self.client.post("/api/auth/login", json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.is_json)
        self.assertFalse(response.json["success"])

    def test_login_correct_credentials_returns_tokens(self):
        """
        Test: correct credentials return an access token and a refresh token.
        """
        payload = {
            "email": "user@example.com",
            "password": "correctpassword123",
        }
        mock_user = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user@example.com",
            "username": "testuser",
            "password_hash": "$2b$12$hashedpasswordhere",
            "created_at": "2026-07-30T00:00:00",
        }
        with patch(
            "app.api.auth.repository.find_user_by_email", return_value=mock_user
        ):
            with patch("app.api.auth.service.check_password", return_value=True):
                with patch(
                    "app.api.auth.repository.create_session",
                    return_value={"id": 1},
                ) as mock_create_session:
                    response = self.client.post("/api/auth/login", json=payload)

                    self.assertEqual(response.status_code, 200)
                    self.assertTrue(response.is_json)
                    self.assertTrue(response.json["success"])
                    self.assertIn("access_token", response.json["data"])
                    self.assertIn("refresh_token", response.json["data"])
                    self.assertTrue(mock_create_session.called)


if __name__ == "__main__":
    unittest.main()
