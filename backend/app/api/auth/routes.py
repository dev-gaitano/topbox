from flask import Blueprint, Response, jsonify, request

from app.models.user import User
from .repository import DuplicateUserError
from .service import ValidationError, handle_signup

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/signup")
def signup_route() -> tuple[Response, int]:
    username, email, password, confirmed_password = User.handle_signup_data(
        request.get_json() or {}
    )

    try:
        user_data = handle_signup(
            username=username,
            email=email,
            password=password,
            confirmed_password=confirmed_password,
        )
        return (
            jsonify(
                {
                    "success": True,
                    "message": "User registered successfully",
                    "data": user_data,
                }
            ),
            201,
        )
    except ValidationError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except DuplicateUserError as e:
        return jsonify({"success": False, "message": str(e)}), 409
    except Exception as e:
        print(f"Error fetching companies: {e}")
        return jsonify({"success": False, "message": "Failed to create user"}), 500
