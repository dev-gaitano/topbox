from datetime import datetime, timedelta, timezone

import hashlib
import secrets
import bcrypt
from flask import current_app

from app.utils.jwt_utils import generate_access_token
from . import repository
from .repository import DuplicateUserError


class ValidationError(Exception):
    pass


class AuthenticationError(Exception):
    pass


def handle_signup(
    username: str, email: str, password: str, confirmed_password: str
) -> dict:
    if not username or not username.strip():
        raise ValidationError("Username is required")
    if not email or not email.strip():
        raise ValidationError("Email is required")
    if not password:
        raise ValidationError("Password is required")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")

    if password != confirmed_password:
        raise ValidationError("Password and confirmed_password do not match")

    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14))
    password_hash = hashed_bytes.decode("utf-8")

    try:
        return repository.signup(
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=password_hash,
        )
    except DuplicateUserError as e:
        raise e


def check_password(plain_password: str, password_hash: str) -> bool:
    if not plain_password or not password_hash:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), password_hash.encode("utf-8")
        )
    except Exception:
        return False


def issue_tokens(
    user_id: str,
    email: str,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> dict:
    """Create an access/refresh token pair and persist the session.
    Shared by login now, and by refresh later."""
    secret_key = current_app.config["JWT_SECRET_KEY"]
    access_token_expires = int(current_app.config["ACCESS_TOKEN_EXPIRES_MINUTES"])
    refresh_token_expires_days = int(current_app.config["REFRESH_TOKEN_EXPIRES_DAYS"])

    access_token = generate_access_token(
        user_id=user_id,
        email=email,
        secret_key=secret_key,
        expires_in_minutes=access_token_expires,
    )

    refresh_token = secrets.token_urlsafe(32)
    refresh_token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(days=refresh_token_expires_days)

    repository.create_session(
        user_id=user_id,
        refresh_token_hash=refresh_token_hash,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def handle_login(
    email: str,
    password: str,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> dict:
    if not email or not email.strip():
        raise ValidationError("Email is required")
    if not password:
        raise ValidationError("Password is required")

    user = repository.find_user_by_email(email.strip().lower())
    if not user:
        raise AuthenticationError("Invalid email or password")
    if not check_password(password, user["password_hash"]):
        raise AuthenticationError("Invalid email or password")

    tokens = issue_tokens(
        user_id=user["id"],
        email=user["email"],
        user_agent=user_agent,
        ip_address=ip_address,
    )

    return {
        **tokens,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"],
        },
    }


def _hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


def _session_is_expired(session: dict) -> bool:
    expires_at = session.get("expires_at")
    if expires_at is None:
        return True
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at <= datetime.now(timezone.utc)


def handle_logout(refresh_token: str) -> None:
    if not refresh_token or not str(refresh_token).strip():
        raise ValidationError("Refresh token is required")

    token_hash = _hash_refresh_token(refresh_token.strip())
    session = repository.find_session_by_refresh_token(token_hash)
    if not session:
        raise AuthenticationError("Invalid refresh token")
    if session.get("revoked_at"):
        return

    repository.revoke_session(session["id"])


def handle_refresh(
    refresh_token: str,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> dict:
    if not refresh_token or not str(refresh_token).strip():
        raise ValidationError("Refresh token is required")

    token_hash = _hash_refresh_token(refresh_token.strip())
    session = repository.find_session_by_refresh_token(token_hash)
    if not session or session.get("revoked_at") or _session_is_expired(session):
        raise AuthenticationError("Invalid refresh token")

    user = repository.find_user_by_id(session["user_id"])
    if not user:
        raise AuthenticationError("Invalid refresh token")

    repository.revoke_session(session["id"])
    return issue_tokens(
        user_id=user["id"],
        email=user["email"],
        user_agent=user_agent,
        ip_address=ip_address,
    )
