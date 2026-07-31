import json
from typing import Any

from app.database.connection import db_connection
from app.models import Company

COMPANY_COLUMNS = """
    id, user_id, name, logo, industry, email, description,
    target_audience, color_palette, unique_value,
    main_competitors, personality, tone, created_at
"""


def get_all(user_id: str) -> list[dict]:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            SELECT {COMPANY_COLUMNS}
            FROM companies
            WHERE user_id = %s
            ORDER BY created_at;
            """,
            (user_id,),
        )
        rows = cursor.fetchall() or []
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, r)) for r in rows]

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_by_id(company_id: int, user_id: str) -> dict[str, Any] | None:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            SELECT {COMPANY_COLUMNS}
            FROM companies
            WHERE id = %s AND user_id = %s;
            """,
            (company_id, user_id),
        )
        row = cursor.fetchone()
        if not row:
            return None

        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create(company: Company, user_id: str) -> dict[str, Any]:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO companies (
                user_id,
                name,
                logo,
                industry,
                email,
                description,
                target_audience,
                color_palette,
                unique_value,
                main_competitors,
                personality,
                tone
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s::jsonb, %s,
                %s::jsonb, %s::jsonb, %s
            )
            RETURNING id, name, created_at;
            """,
            (user_id, *company.to_db_params()),
        )

        row = cursor.fetchone()
        conn.commit()

        return {
            "id": row[0],
            "name": row[1],
            "created_at": row[2].isoformat(),
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete(company_id: int, user_id: str) -> dict[str, Any] | None:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM companies
            WHERE id = %s AND user_id = %s
            RETURNING id, name, created_at
            """,
            (company_id, user_id),
        )

        row = cursor.fetchone()
        conn.commit()
        if not row:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "created_at": row[2].isoformat() if row[2] else None,
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update(
    changed_fields: dict, company_id: int, user_id: str
) -> dict[str, Any] | None:
    conn = db_connection()
    cursor = conn.cursor()

    set_clauses = []
    values = []

    for col, val in changed_fields.items():
        if col in ("color_palette", "main_competitors", "personality"):
            set_clauses.append(f"{col} = %s::jsonb")
            values.append(json.dumps(val))
        else:
            set_clauses.append(f"{col} = %s")
            values.append(val)

    values.extend([company_id, user_id])
    query = f"""
        UPDATE companies
        SET {', '.join(set_clauses)}
        WHERE id = %s AND user_id = %s
        RETURNING id, name, created_at;
    """

    try:
        cursor.execute(query, tuple(values))
        row = cursor.fetchone()
        conn.commit()
        if not row:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "updated_at": row[2].isoformat() if row[2] else None,
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
