import bcrypt

from . import repository
from .repository import DuplicateUserError


class ValidationError(Exception):
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

    hashed_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
    password_hash = hashed_bytes.decode("utf-8")

    try:
        return repository.signup(
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=password_hash,
        )
    except DuplicateUserError as e:
        raise e
