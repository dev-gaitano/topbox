from flask import Blueprint, Response

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/signup")
def signup_route() -> tuple[Response, int]:
    pass
