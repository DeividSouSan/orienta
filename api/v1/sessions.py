import os

from dotenv import load_dotenv
from flask import Blueprint, Response, make_response, request

from dtos.session_request import SessionRequest
from models import auth, session

load_dotenv()

session_bp = Blueprint("sessions", __name__)

ENV = os.getenv("ENVIRONMENT", "development")


@session_bp.route("/sessions", methods=["POST"])
def create() -> Response:
    req = SessionRequest.from_dict(request.get_json())

    auth_user = auth.authenticate(email=req.email, password=req.password)

    session_cookie = session.create(auth_user)

    response = make_response(
        {
            "message": "Sessão criada com sucesso.",
        },
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
    response = make_response(
        {
            "message": "Sessão encerrada com sucesso.",
        },
        200,
    )
    response.delete_cookie("session_id", path="/")

    return response
