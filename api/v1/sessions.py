import os
from flask import Blueprint, Response, jsonify, make_response, request

from errors import UnauthorizedError
from models import auth, session
from dotenv import load_dotenv

load_dotenv()

session_bp = Blueprint("sessions", __name__)

ENV = os.getenv("ENVIRONMENT", "development")


@session_bp.route("/sessions", methods=["POST"])
def create() -> Response:
    data = request.get_json()

    authenticated_user = auth.authenticate(
        email=data.get("email", ""), password=data.get("password", "")
    )

    session_cookie = session.create(authenticated_user["idToken"])

    response = make_response(
        jsonify(
            {
                "message": "Sessão criada com sucesso.",
                "data": {
                    "userId": authenticated_user["localId"],
                    "username": authenticated_user["displayName"],
                    "email": authenticated_user["email"],
                    "sessionCookie": session_cookie,
                    "sessionExpiresIn": session.DURATION_IN_SECONDS,
                },
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


@session_bp.route("/sessions", methods=["DELETE"])
def delete() -> Response:
    response = make_response(jsonify({"message": "Sessão encerrada com sucesso."}), 200)
    response.delete_cookie("session_id", path="/")

    return response
