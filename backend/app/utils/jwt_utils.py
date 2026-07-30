from datetime import datetime, timedelta, timezone
from typing import Any
import jwt


def encode_jwt(payload: dict[str, Any], secret: str) -> str:
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_jwt(token: str, secret: str) -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=["HS256"])


def generate_access_token(
    user_id: str, email: str, secret_key: str, expires_in_minutes: int = 15
) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_in_minutes)
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": exp,
        "type": "access",
    }
    return encode_jwt(payload, secret_key)
