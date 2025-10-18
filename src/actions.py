from flask import Blueprint, jsonify

from firebase_admin import firestore

api = Blueprint("api", __name__)


@api.route("/guides/<string:id>/<int:day>", methods=["POST"])
def toggle_complete(id: str, day: int):
    print("Chegou aqui")
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
