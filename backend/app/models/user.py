from datetime import datetime
from typing import Any


class User:
    def __init__(
        self,
        username: str,
        email: str,
        password_hash: str,
        id: str | None = None,
        created_at: datetime | str | None = None,
    ) -> None:
        fields: dict[str, tuple[Any, type]] = {
            "username": (username, str),
            "email": (email, str),
            "password_hash": (password_hash, str),
        }

        for field_name, (value, expected_type) in fields.items():
            if not isinstance(value, expected_type):
                raise TypeError(f"Invalid data type for {field_name}")

        if not username.strip() or not email.strip() or not password_hash:
            raise ValueError("Missing required fields: username, email, password_hash")

        self.id = id
        self.username = username.strip()
        self.email = email.strip().lower()
        self.password_hash = password_hash
        self.created_at = created_at

    @classmethod
    def handle_signup_data(cls, data: dict[str, Any]) -> tuple[str, str, str, str]:
        data = data or {}
        username = data.get("username", "")
        email = data.get("email", "")
        password = data.get("password", "")
        confirmed_password = (
            data.get("confirmed_password") or data.get("confirm_password") or ""
        )
        return username, email, password, confirmed_password

    @classmethod
    def handle_login_data(cls, data: dict[str, Any]) -> tuple[str, str]:
        data = data or {}
        email = data.get("email", "")
        password = data.get("password", "")
        return email, password

    def to_db_params(self) -> tuple[str, str, str]:
        return (
            self.username,
            self.email,
            self.password_hash,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id) if self.id else None,
            "username": self.username,
            "email": self.email,
            "created_at": (
                self.created_at.isoformat()
                if isinstance(self.created_at, datetime)
                else self.created_at
            ),
        }
