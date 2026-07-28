from . import repository
from app.models import Company


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
    company = Company.handle_request_data(data)

    return repository.update(company, id)
