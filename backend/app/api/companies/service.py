from . import repository
from app.models import Company

FIELD_MAP = {
    "businessName": "name",
    "logo": "logo",
    "industry": "industry",
    "email": "email",
    "description": "description",
    "targetAudience": "target_audience",
    "uniqueValue": "unique_value",
    "tone": "tone",
    "colorPalette": "color_palette",
    "mainCompetitors": "main_competitors",
    "personality": "personality",
}


def get_companies(user_id: str):
    return repository.get_all(user_id)


def get_company(company_id: int, user_id: str):
    return repository.get_by_id(company_id, user_id)


def create_company(data: dict, user_id: str):
    company = Company.handle_request_data(data)
    return repository.create(company, user_id)


def delete_company(company_id: int, user_id: str):
    return repository.delete(company_id, user_id)


def update_company(data: dict, company_id: int, user_id: str):
    current = repository.get_by_id(company_id, user_id)

    if not current:
        return None

    changed = {}

    for key, new_val in data.items():
        db_col = FIELD_MAP.get(key)

        if not db_col:
            continue

        old_val = current.get(db_col)

        if new_val != old_val:
            changed[db_col] = new_val

    if not changed:
        return {
            "id": current["id"],
            "name": current["name"],
            "updated_at": current.get("updated_at"),
        }

    return repository.update(changed, company_id, user_id)
