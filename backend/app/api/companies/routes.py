from typing import Any
from flask import Blueprint, Response, request, jsonify

from .service import (
    delete_company,
    get_companies,
    get_company,
    create_company,
    update_company,
)

companies_bp = Blueprint("companies", __name__)


@companies_bp.get("")
def get_companies_route() -> tuple[Response, int]:
    try:
        companies = get_companies()

        return jsonify(companies), 200

    except Exception as e:
        print(f"Error fetching companies: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Failed to fetch companies",
                }
            ),
            500,
        )


@companies_bp.get("/<int:company_id>")
def get_company_route(company_id: int) -> tuple[Response, int]:
    try:
        company = get_company(company_id)
        if not company:
            return jsonify({"success": False, "message": "Company not found"}), 404

        return jsonify(company), 200

    except Exception as e:
        print(f"Error fetching company: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Failed to fetch company",
                }
            ),
            500,
        )


@companies_bp.post("")
def create_company_route() -> tuple[Response, int]:
    try:
        payload = request.get_json(silent=True)

        if not payload:
            return jsonify({"success": False, "message": "No JSON data provided"}), 400

        company = create_company(payload)

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Company created successfully",
                    "data": company,
                }
            ),
            201,
        )

    except Exception as e:
        print(f"Error creating company: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Failed to create company",
                }
            ),
            500,
        )


@companies_bp.delete("/<int:company_id>")
def delete_company_route(company_id: int) -> tuple[Response, int]:
    try:
        company = delete_company(company_id)

        return jsonify(company), 200

    except Exception as e:
        print(f"Error deleting company: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Failed to delete company",
                }
            ),
            500,
        )


@companies_bp.patch("/<int:company_id>")
def update_company_route(company_id: int) -> tuple[Response, int]:
    try:
        # Get data from input
        payload: dict[str, Any] | None = request.get_json(silent=True)

        if not payload:
            return jsonify({"success": False, "message": "No JSON data provided"}), 400

        company = update_company(payload, company_id)

        return jsonify(company), 200

    except Exception as e:
        print(f"Error updating company: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Failed to update company",
                }
            ),
            500,
        )
