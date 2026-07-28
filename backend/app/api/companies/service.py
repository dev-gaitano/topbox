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


def get_companies():
    return repository.get_all()


def get_company(id: int):
    return repository.get_by_id(id)


def create_company(data: dict):
    company = Company.handle_request_data(data)

    return repository.create(company)


def delete_company(id: int):
    company = repository.delete(id)

    return company


def update_company(data: dict, id: int):
    current = repository.get_by_id(id)

    if not current:
        return None

    changed = {}

    for key, new_val in data.items():
        db_col = FIELD_MAP.get(key)

        # ignore unknown fields
        if not db_col:
            continue

        old_val = current.get(db_col)

        # Check what changed
        if new_val != old_val:
            changed[db_col] = new_val

    if not changed:
        return {
            "id": current["id"],
            "name": current["name"],
            "updated_at": current.get("updated_at"),
        }

    return repository.update(changed, id)
