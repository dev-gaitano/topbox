from functools import wraps
from typing import Any, Callable

from flask import current_app, g, jsonify, request

from app.api.auth import repository
from app.utils.jwt_utils import TokenError, verify_access_token


def require_auth(view: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Missing or invalid authorization header",
                    }
                ),
                401,
            )

        token = auth_header[len("Bearer ") :].strip()
        if not token:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Missing or invalid authorization header",
                    }
                ),
                401,
            )

        try:
            payload = verify_access_token(
                token=token,
                secret_key=current_app.config["JWT_SECRET_KEY"],
            )
        except TokenError as e:
            return jsonify({"success": False, "message": str(e)}), 401

        session = repository.find_session_by_id(payload["sid"])

        if not session or session.get("revoked_at") is not None:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Session has been revoked",
                    }
                ),
                401,
            )

        if str(session["user_id"]) != str(payload["sub"]):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Invalid token payload",
                    }
                ),
                401,
            )

        g.current_user_id = payload["sub"]
        g.current_user_email = payload.get("email")
        g.current_session_id = payload["sid"]
        g.jwt_payload = payload
        return view(*args, **kwargs)

    return wrapped
