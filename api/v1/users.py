from flask import Blueprint, Response, jsonify, request, make_response

from models import user

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create_user() -> Response:
    data = request.get_json()

    newUser = user.create(
        username=data.get("username", ""),
        email=data.get("email", ""),
        password=data.get("password", ""),
    )

    return make_response(jsonify(newUser), 200)
