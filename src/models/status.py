from firebase_admin import firestore


def check() -> str | None:
    try:
        db = firestore.client()
        doc_ref = db.collection("_internal_status").document("health_check")
        doc_ref.get()

        return "Online"
    except Exception as error:
        print(error)
        return "Offline"
