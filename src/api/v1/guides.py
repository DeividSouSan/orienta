from flask import Blueprint, jsonify, make_response, request, g


from src.models import guide
from src.utils import protected

guides_bp = Blueprint("guides", __name__)


@guides_bp.route("/guides", methods=["POST"])
@protected
def create():
    data = request.get_json()

    guide_info = {
        "title": data.get("title", ""),
        "temperature": data.get("temperature", 2.0),
        "model": data.get("model", ""),
        "inputs": {
            "topic": data.get("topic", ""),
            "knowledge": data.get("knowledge", ""),
            "focus_time": data.get("focus_time", ""),
            "days": data.get("days", ""),
        },
    }

    study_guide: dict = guide.generate_with_metadata(
        owner=g.username,
        title=guide_info["title"],
        inputs=guide_info["inputs"],
        model=guide_info["model"],
        temperature=guide_info["temperature"],
    )

    guide.save(study_guide)

    print("O resultado é: ", study_guide)

    return make_response(
        jsonify(
            {"message": "Guia de estudos gerado com sucesso.", "data": study_guide}
        ),
        201,
    )


@guides_bp.route("/guides/<string:guide_id>", methods=["DELETE"])
@protected
def delete(guide_id: str):
    guide.delete(guide_id, g.username)

    return make_response(
        jsonify({"message": "Guia de estudo deletado com sucesso."}), 200
    )


@guides_bp.route("/guides/<string:guide_id>", methods=["GET"])
@protected
def get_guides_by_id(guide_id: str):
    # recuperar o guia por id
    study_guide = guide.find_guide_by_id(guide_id)

    return {"message": "Guia recuperado com sucesso.", "data": study_guide}


@guides_bp.route("/guideline/<string:guide_id>", methods=["GET"])
@protected
def get_guideline_by_id(guide_id: str):
    user_guides: list[dict] = guide.find_guideline_by_id(guide_id)

    return make_response(
        {"message": "Guideline recuperada com sucesso.", "data": user_guides}, 200
    )


@guides_bp.route("/guides", methods=["GET"])
@protected
def get_my_guides():
    user_guides: list[dict] = guide.find_by_username(g.username)

    return make_response(
        {"message": "Guias recuperados com sucesso.", "data": user_guides}, 200
    )


@guides_bp.route("/guides/<string:guide_id>", methods=["PATCH"])
@protected
def toggle_complete(guide_id: str):
    data = request.get_json()

    new_studies_list = data.get("new_studies_list", "")
    db_studies_data: list = guide.update_studies(guide_id, new_studies_list, g.username)

    return make_response(
        {
            "message": "O estado da Studies List foi alterado com sucesso!",
            "data": db_studies_data,
        },
        200,
    )
