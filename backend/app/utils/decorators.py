from functools import wraps
from typing import Any, Callable

from flask import current_app, g, jsonify, request

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

        g.current_user_id = payload["sub"]
        g.current_user_email = payload.get("email")
        g.jwt_payload = payload
        return view(*args, **kwargs)

    return wrapped
