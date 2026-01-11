from flask import Blueprint, Response

from models import status

status_bp = Blueprint("status", __name__)


@status_bp.route("/status", methods=["GET"])
def get_status() -> Response:
    api_status = status.check()

    return (
        {
            "message": "API está online."
            if api_status == "Online"
            else "API está offline.",
            "data": {"status": api_status},
        },
        200 if api_status == "Online" else 503,
    )
