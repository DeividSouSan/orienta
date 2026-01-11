from flask import Blueprint, Response, request

from models import prompt
from utils import protected

validations_bp = Blueprint("validate", __name__)


@validations_bp.route("/validations/topic", methods=["POST"])
@protected
def validate_topic() -> Response:
    data = request.get_json()

    topic = data.get("topic", "").strip()

    prompt.validate_topic(topic)
    result = prompt.validate_relevance(topic)

    return {
        "message": "O tópico é válido.",
        "data": {"topic": topic, "info": result.model_dump()},
    }, 200
