from flask import Blueprint, Response, request

from models import prompt
from objects.topic import Topic
from utils import protected

validations_bp = Blueprint("validate", __name__)


@validations_bp.route("/validations/topic", methods=["POST"])
@protected
def validate_topic() -> Response:
    data = request.get_json()

    topic_str = data.get("topic", "").strip()

    # Validação sintática via VO
    topic = Topic(topic_str)

    # Validação semântica via IA — recebe o VO diretamente
    prompt.validate_relevance(topic)

    return {
        "message": "O tópico é válido.",
    }, 200
