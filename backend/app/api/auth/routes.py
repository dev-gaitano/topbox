from flask import Blueprint, Response, jsonify, request

from app.models.user import User
from .repository import DuplicateUserError
from .service import AuthenticationError, ValidationError, handle_login, handle_signup

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
        print(f"Error signing up user: {e}")
        return jsonify({"success": False, "message": "Failed to create user"}), 500


@auth_bp.post("/login")
def login_route() -> tuple[Response, int]:
    email, password = User.handle_login_data(request.get_json() or {})
    user_agent = request.headers.get("User-Agent")
    ip_address = request.remote_addr

    try:
        data = handle_login(
            email=email,
            password=password,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Login successful",
                    "data": data,
                }
            ),
            200,
        )
    except ValidationError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except AuthenticationError as e:
        return jsonify({"success": False, "message": str(e)}), 401
    except Exception as e:
        print(f"Error logging in user: {e}")
        return jsonify({"success": False, "message": "Failed to login"}), 500
