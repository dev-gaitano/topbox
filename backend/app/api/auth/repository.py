from app.database.connection import db_connection
from app.models.user import User


class DuplicateUserError(Exception):
    pass


def signup(username: str, email: str, password_hash: str) -> dict:
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
            "created_at": row[3].isoformat() if hasattr(row[3], "isoformat") else str(row[3]),
        }
    except Exception as e:
        conn.rollback()
        err_msg = str(e).lower()
        if "unique" in err_msg or "duplicate" in err_msg or "idx_users" in err_msg:
            raise DuplicateUserError("User with given username or email already exists") from e
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
