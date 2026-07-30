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

    # Check if user exists
    user = repository.find_user_by_email(email.strip().lower())

    if not user:
        raise AuthenticationError("Invalid email or password")

    if not check_password(password, user["password_hash"]):
        raise AuthenticationError("Invalid email or password")

    # Generate access and refresh tokens
    secret_key = current_app.config["JWT_SECRET_KEY"]
    access_token_expires = int(current_app.config["ACCESS_TOKEN_EXPIRES_MINUTES"])
    refresh_token_expires_days = int(current_app.config["REFRESH_TOKEN_EXPIRES_DAYS"])

    access_token = generate_access_token(
        user_id=user["id"],
        email=user["email"],
        secret_key=secret_key,
        expires_in_minutes=access_token_expires,
    )

    refresh_token = secrets.token_urlsafe(32)
    refresh_token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()

    expires_at = datetime.now(timezone.utc) + timedelta(days=refresh_token_expires_days)

    # Create user session
    repository.create_session(
        user_id=user["id"],
        refresh_token_hash=refresh_token_hash,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"],
        },
    }
