from flask import Blueprint, jsonify, make_response, request

from models import prompt
from utils import protected

validations_bp = Blueprint("validate", __name__)


@validations_bp.route("/validate/topic", methods=["POST"])
@protected
def validate():
    data = request.get_json()
    topic = data.get("topic", "")

    prompt.validate_topic(topic)
    prompt.validate_relevance(topic)

    return make_response(
        jsonify(
            {
                "message": "O tópico é válido.",
                "data": {
                    "topic": topic,
                },
            }
        ),
        200,
    )
