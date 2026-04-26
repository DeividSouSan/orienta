from flask import Blueprint, Response, g, request

from dtos.guide_request import GuideRequest
from models import guide
from objects.guide_id import GuideId
from objects.username import Username
from utils import protected

guides_bp = Blueprint("guides", __name__)


@guides_bp.route("/guides", methods=["POST"])
@protected
def create() -> Response:
    guide_request = GuideRequest.from_dict(request.get_json())

    study_guide = guide.generate_with_metadata(
        owner=Username(g.username),
        inputs=guide_request,
    )

    saved_guide = guide.save(study_guide)

    return {
        "message": "Guia de estudos gerado com sucesso.",
        "data": saved_guide.to_dict(),
    }, 201


@guides_bp.route("/guides/<string:guide_id>", methods=["DELETE"])
@protected
def delete(guide_id: str) -> Response:
    guide.delete(GuideId(guide_id), Username(g.username))

    return {
        "message": "Guia de estudo deletado com sucesso.",
    }, 200


@guides_bp.route("/guides/<string:guide_id>", methods=["GET"])
@protected
def get_by_id(guide_id: str) -> Response:
    study_guide = guide.find_by_id(GuideId(guide_id))

    return {
        "message": "Guia recuperado com sucesso.",
        "data": study_guide.to_dict(),
    }, 200


@guides_bp.route("/my-guides", methods=["GET"])
@protected
def get_my_guides() -> Response:
    user_guides = guide.find_all_by_username(Username(g.username))

    return {
        "message": "Guias recuperados com sucesso.",
        "data": [g.to_dict() for g in user_guides],
    }, 200


@guides_bp.route("/guides/<string:guide_id>", methods=["PATCH"])
@protected
def toggle_complete(guide_id: str) -> Response:
    data = request.get_json()

    new_studies_list = data.get("new_studies_list", "")
    db_studies_data: list = guide.update_studies(
        GuideId(guide_id), new_studies_list, Username(g.username)
    )

    return {
        "message": "O estado da Studies List foi alterado com sucesso!",
        "data": db_studies_data,
    }, 200
