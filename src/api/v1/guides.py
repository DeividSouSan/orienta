from flask import Blueprint, jsonify, make_response, request, g

from firebase_admin import firestore

from src.models import guide, user
from src.utils import protected

guides_bp = Blueprint("guides", __name__)


@guides_bp.route("/guides", methods=["POST"])
@protected
def create():
    data = request.get_json()
    guide_inputs = {
        "topic": data.get("topic", ""),
        "knowledge": data.get("knowledge", ""),
        "focus_time": data.get("focus_time", ""),
        "days": data.get("days", ""),
    }

    model_inputs = {
        "model": data.get("model", ""),
        "temperature": data.get("temperature", 2),
    }

    study_guide: dict = guide.generate_with_metadata(
        owner=g.username,
        inputs=guide_inputs,
        model=model_inputs["model"],
        temperature=model_inputs["temperature"],
    )

    guide.save(study_guide)

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


@guides_bp.route("/guides/<string:username>", methods=["GET"])
@protected
def get_public_guides_by_username(username: str):
    found_user = user.find_by_username(username)

    user_guides: list[dict] = guide.find_by_username(
        found_user["username"], only_public=True
    )

    return make_response(
        {"message": "Guias recuperados com sucesso.", "data": user_guides}, 200
    )


@guides_bp.route("/guideline/<string:guide_id>", methods=["GET"])
@protected
def get_guideline_by_id(guide_id: str):
    user_guides: list[dict] = guide.find_guideline_by_id(guide_id)

    return make_response(
        {"message": "Guideline recuperada com sucesso.", "data": user_guides}, 200
    )


@guides_bp.route("/my-guides", methods=["GET"])
@protected
def get_my_guides():
    user_guides: list[dict] = guide.find_by_username(g.username)

    return make_response(
        {"message": "Guias recuperados com sucesso.", "data": user_guides}, 200
    )


@guides_bp.route("/guides/<string:id>/<int:day>", methods=["POST"])
def toggle_complete(id: str, day: int):
    db = firestore.client()

    study_day_ref = (
        db.collection("study_guides")
        .document(id)
        .collection("daily_plans")
        .document(f"Study_{day}")
    )

    study_day = study_day_ref.get()

    if study_day.to_dict().get("done", False):
        study_day_ref.update({"done": False})
    else:
        study_day_ref.update({"done": True})

    return jsonify(study_day_ref.get().to_dict())
