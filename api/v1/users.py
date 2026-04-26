from flask import Blueprint, Response, request

from dtos.user_create_request import UserCreateRequest
from models import user

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create() -> Response:
    user_request = UserCreateRequest.from_dict(request.get_json())

    new_user = user.create(user_request)

    return {
        "message": "Usuário criado com sucesso.",
        "data": new_user.to_dict(),
    }, 201
