from datetime import datetime, timedelta, timezone
from typing import Any
import jwt


class TokenError(Exception):
    pass


def encode_jwt(payload: dict[str, Any], secret: str) -> str:
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_jwt(token: str, secret: str) -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=["HS256"])


def generate_access_token(
    user_id: str,
    email: str,
    secret_key: str,
    session_id: int,
    expires_in_minutes: int = 15,
) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_in_minutes)
    payload = {
        "sub": str(user_id),
        "email": email,
        "sid": session_id,
        "iat": now,
        "exp": exp,
        "type": "access",
    }
    return encode_jwt(payload, secret_key)


def verify_access_token(token: str, secret_key: str) -> dict[str, Any]:
    if not token or not secret_key:
        raise TokenError("Missing token or secret key")

    try:
        payload = decode_jwt(token, secret_key)
    except jwt.ExpiredSignatureError as e:
        raise TokenError("Token has expired") from e
    except jwt.InvalidSignatureError as e:
        raise TokenError("Invalid token signature") from e
    except jwt.InvalidTokenError as e:
        raise TokenError("Invalid token") from e

    if payload.get("type") != "access":
        raise TokenError("Invalid token type")
    if not payload.get("sub"):
        raise TokenError("Invalid token payload")
    if payload.get("sid") is None:
        raise TokenError("Invalid token payload")

    return payload
