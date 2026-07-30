from datetime import datetime
from typing import Any
from app.database.connection import db_connection
from app.models.user import User


class DuplicateUserError(Exception):
    pass


def signup(username: str, email: str, password_hash: str) -> dict[str, Any]:
    user = User(username=username, email=email, password_hash=password_hash)
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, username, email, created_at;
            """,
            user.to_db_params(),
        )
        row = cursor.fetchone()
        conn.commit()

        return {
            "id": str(row[0]),
            "username": row[1],
            "email": row[2],
            "created_at": (
                row[3].isoformat() if hasattr(row[3], "isoformat") else str(row[3])
            ),
        }

    except Exception as e:
        conn.rollback()
        err_msg = str(e).lower()
        if "unique" in err_msg or "duplicate" in err_msg or "idx_users" in err_msg:
            raise DuplicateUserError(
                "User with given username or email already exists"
            ) from e
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def find_user_by_email(email: str) -> dict[str, Any] | None:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, username, email, password_hash, created_at
            FROM users
            WHERE LOWER(email) = LOWER(%s);
            """,
            (email.strip(),),
        )
        row = cursor.fetchone()
        if not row:
            return None

        return {
            "id": str(row[0]),
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
            "created_at": (
                row[4].isoformat() if hasattr(row[4], "isoformat") else str(row[4])
            ),
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_session(
    user_id: str,
    refresh_token_hash: str,
    expires_at: datetime,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> dict[str, Any]:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO sessions (user_id, refresh_token_hash, expires_at, user_agent, ip_address)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, user_id, refresh_token_hash, created_at, expires_at;
            """,
            (user_id, refresh_token_hash, expires_at, user_agent, ip_address),
        )
        row = cursor.fetchone()
        conn.commit()

        return {
            "id": row[0],
            "user_id": str(row[1]),
            "refresh_token_hash": row[2],
            "created_at": (
                row[3].isoformat() if hasattr(row[3], "isoformat") else str(row[3])
            ),
            "expires_at": (
                row[4].isoformat() if hasattr(row[4], "isoformat") else str(row[4])
            ),
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
