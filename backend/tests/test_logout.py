import unittest
from unittest.mock import patch
from app import create_app


class TestLogout(unittest.TestCase):
    def setUp(self):
        self.flask_app = create_app()
        self.flask_app.config["TESTING"] = True
        self.client = self.flask_app.test_client()

    def test_logout_marks_session_revoked_and_refresh_fails(self):
        """
        Test: logout marks the session revoked and a subsequent refresh
        with that token fails.
        """
        refresh_token = "logout-then-refresh-token"
        mock_session = {
            "id": 1,
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "refresh_token_hash": "hashed-refresh-token",
            "created_at": "2026-07-30T00:00:00",
            "expires_at": "2026-08-30T00:00:00",
            "revoked_at": None,
        }

        with patch(
            "app.api.auth.repository.find_session_by_refresh_token",
            return_value=mock_session,
            create=True,
        ):
            with patch(
                "app.api.auth.repository.revoke_session",
                return_value={
                    **mock_session,
                    "revoked_at": "2026-07-31T09:00:00",
                },
                create=True,
            ) as mock_revoke:
                logout_response = self.client.post(
                    "/api/auth/logout",
                    json={"refresh_token": refresh_token},
                )

                self.assertEqual(logout_response.status_code, 200)
                self.assertTrue(logout_response.is_json)
                self.assertTrue(logout_response.json["success"])
                self.assertTrue(mock_revoke.called)

        revoked_session = {
            **mock_session,
            "revoked_at": "2026-07-31T09:00:00",
        }
        with patch(
            "app.api.auth.repository.find_session_by_refresh_token",
            return_value=revoked_session,
            create=True,
        ):
            refresh_response = self.client.post(
                "/api/auth/refresh",
                json={"refresh_token": refresh_token},
            )

            self.assertEqual(refresh_response.status_code, 401)
            self.assertTrue(refresh_response.is_json)
            self.assertFalse(refresh_response.json["success"])


if __name__ == "__main__":
    unittest.main()
