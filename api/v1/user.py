from flask import Blueprint, Response, g

from models import user
from utils import protected

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@protected
def me() -> Response:
    current_user = user.find_by_username(g.username)

    return {
        "message": "Usuário atual recuperado com sucesso.",
        "data": current_user,
    }, 200
