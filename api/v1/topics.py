from flask import Blueprint, Response, request

from dtos.topic import Topic
from utils import protected

topics_bp = Blueprint("topics", __name__)


@topics_bp.route("/topics/check-feasibility", methods=["POST"])
@protected
def check_feasability() -> Response:
    topic = Topic(request.get_json())

    result = topic.check_feasibility()

    return {
        "message": "O tópico foi validado.",
        "data": result,
    }, 200
