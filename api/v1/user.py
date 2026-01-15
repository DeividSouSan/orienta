from flask import Blueprint, Response, g

from utils import protected

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@protected
def me() -> Response:
    return {
        "message": "Usuário atual recuperado com sucesso.",
        "data": {
            "userId": g.uid,
            "username": g.username,
            "email": g.email,
        },
    }, 200
