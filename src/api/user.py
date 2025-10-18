from flask import Blueprint, Response, jsonify, request, make_response


from src.models import user

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["POST"])
def create_user() -> Response:
    data = request.get_json()

    newUser = user.create(
        username=data.get("username", ""),
        email=data.get("email", ""),
        password=data.get("password", ""),
    )

    return make_response(jsonify(newUser), 200)
