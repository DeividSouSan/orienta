from flask import Blueprint, Response, jsonify, make_response, g

from utils import protected
from errors import UnauthorizedError
from models import user

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@protected
def me() -> Response:
    if not g.get("username"):
        raise UnauthorizedError(
            message="Usuário não autenticado.", action="Faça login para continuar."
        )

    current_user = user.find_by_username(g.username)

    return make_response(
        jsonify(
            {
                "message": "Usuário atual recuperado com sucesso.",
                "data": current_user,
            }
        ),
        200,
    )
