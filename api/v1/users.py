from flask import Blueprint, Response, request

from models import user

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create() -> Response:
    data = request.get_json()

    new_user = user.create(
        username=data.get("username", ""),
        email=data.get("email", ""),
        password=data.get("password", ""),
    )

    return {
        "message": "Usuário criado com sucesso.",
        "data": new_user,
    }, 201
