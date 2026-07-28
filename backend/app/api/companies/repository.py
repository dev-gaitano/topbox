from typing import Any

from app.database.connection import db_connection
from app.models import Company


def get_all() -> list[dict]:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        # Get all companies from database
        cursor.execute("""
                       SELECT id, name, logo, industry, email, description,
                       target_audience, color_palette, unique_value,
                       main_competitors, personality, tone, created_at
                       FROM companies ORDER BY created_at;
                       """)
        rows = cursor.fetchall() or []
        columns = [col[0] for col in cursor.description]

        # Store companies in a list of dicts
        companies: list[dict[str, Any]] = [dict(zip(columns, r)) for r in rows]

        return companies

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_by_id(company_id: int) -> dict[str, Any] | None:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, logo, industry, email, description,
                   target_audience, color_palette, unique_value,
                   main_competitors, personality, tone, created_at
            FROM companies WHERE id = %s;
            """,
            (company_id,),
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


def create(company: Company) -> dict[str, Any]:
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO companies (
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
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s::jsonb,
                %s::jsonb,
                %s
            )
            RETURNING id, name, created_at;
            """,
            company.to_db_params(),
        )

        row = cursor.fetchone()

        conn.commit()

        return {
            "id": row[0],
            "name": row[1],
            "created_at": row[2].isoformat(),
        }

    except:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete(company_id: int):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        # Delete company from database
        cursor.execute(
            """
            DELETE FROM companies WHERE id = %s
            RETURNING id, name, created_at
            """,
            (company_id,),
        )

        row = cursor.fetchone()
        conn.commit()

        return {
            "id": row[0],
            "name": row[1],
            "createdAt": row[2].isoformat() if row[2] else None,
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update(company: Company, company_id: int):
    conn = db_connection()
    cursor = conn.cursor()

    try:

        # Update company in database
        cursor.execute(
            """
            UPDATE companies
            SET name = %s, logo = %s, industry = %s, email = %s, description = %s,
                       target_audience = %s, color_palette = %s::jsonb, unique_value = %s,
                       main_competitors = %s::jsonb, personality = %s::jsonb, tone = %s
            WHERE id = %s
            RETURNING id, name, created_at
        """,
            company.to_db_params() + (company_id,),
        )

        row = cursor.fetchone()
        conn.commit()

        return {
            "id": row[0],
            "name": row[1],
            "createdAt": row[2].isoformat() if row[2] else None,
        }

    except:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
