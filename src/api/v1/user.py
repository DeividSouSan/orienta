from flask import Blueprint, Response, jsonify, make_response, g

from src.utils import protected
from src.errors import UnauthorizedError
from src.models import user

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@protected
def get_user() -> Response:
    if not g.get("username"):
        raise UnauthorizedError(
            "Usuário não autenticado.", "Faça login para continuar."
        )

    currentUser = user.find_by_username(g.username)

    return make_response(jsonify(currentUser), 200)
