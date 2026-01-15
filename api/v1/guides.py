from flask import Blueprint, Response, g, request

from dtos.guide_request import GuideRequest
from models import guide
from utils import protected

guides_bp = Blueprint("guides", __name__)


@guides_bp.route("/guides", methods=["POST"])
@protected
def create() -> Response:
    guide_request = GuideRequest.from_dict(request.get_json())

    study_guide: dict = guide.generate_with_metadata(
        owner=g.username,
        inputs=guide_request,
    )

    guide.save(study_guide)

    return {
        "message": "Guia de estudos gerado com sucesso.",
        "data": study_guide,
    }, 201


@guides_bp.route("/guides/<string:guide_id>", methods=["DELETE"])
@protected
def delete(guide_id: str) -> Response:
    guide.delete(guide_id, g.username)

    return {
        "message": "Guia de estudo deletado com sucesso.",
    }, 200


@guides_bp.route("/guides/<string:guide_id>", methods=["GET"])
@protected
def get_by_id(guide_id: str) -> Response:
    study_guide = guide.find_by_id(guide_id)

    return {
        "message": "Guia recuperado com sucesso.",
        "data": study_guide,
    }, 200


@guides_bp.route("/my-guides", methods=["GET"])
@protected
def get_my_guides() -> Response:
    user_guides: list[dict] = guide.find_all_by_username(g.username)

    return {
        "message": "Guias recuperados com sucesso.",
        "data": user_guides,
    }, 200


@guides_bp.route("/guides/<string:guide_id>", methods=["PATCH"])
@protected
def toggle_complete(guide_id: str) -> Response:
    data = request.get_json()

    new_studies_list = data.get("new_studies_list", "")
    db_studies_data: list = guide.update_studies(guide_id, new_studies_list, g.username)

    return {
        "message": "O estado da Studies List foi alterado com sucesso!",
        "data": db_studies_data,
    }, 200
