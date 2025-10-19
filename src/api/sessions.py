import os
from flask import Blueprint, Response, jsonify, make_response, request

from src.errors import UnauthorizedError
from src.models import auth, session
from dotenv import load_dotenv

load_dotenv()

session_bp = Blueprint("sessions", __name__)

ENV = os.getenv("ENVIRONMENT", "development")


@session_bp.route("/sessions", methods=["POST"])
def create_session() -> Response:
    data = request.get_json()

    authenticated_user = auth.authenticate(
        email=data.get("email", ""), password=data.get("password", "")
    )

    session_cookie = session.create(authenticated_user["idToken"])

    response = make_response(
        jsonify(
            {
                "userId": authenticated_user["localId"],
                "username": authenticated_user["displayName"],
                "email": authenticated_user["email"],
                "sessionCookie": session_cookie,
                "sessionExpiresIn": session.DURATION_IN_SECONDS,
            }
        ),
        201,
    )

    response.set_cookie(
        key="session_id",
        value=session_cookie,
        max_age=session.DURATION_IN_SECONDS,
        httponly=True,
        path="/",
        secure=ENV == "production",
    )

    return response


@session_bp.route("/sessions", methods=["GET"])
def verify_session() -> Response:
    session_cookie = request.cookies.get("session_id", "")

    if not session_cookie:
        raise UnauthorizedError("Não há sessão ativa.", "Faça login para continuar.")

    decoded_token = session.verify(session_cookie)
    return make_response(
        jsonify(
            {
                "userId": decoded_token["uid"],
                "username": decoded_token["name"],
                "email": decoded_token["email"],
            }
        ),
        200,
    )


@session_bp.route("/sessions", methods=["DELETE"])
def delete_session() -> Response:
    response = make_response(jsonify({"message": "Sessão encerrada com sucesso."}), 200)
    response.delete_cookie("session_id", path="/")

    return response
