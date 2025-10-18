from dotenv import load_dotenv
import firebase_admin
from firebase_admin import firestore

load_dotenv()


def initialize_app():
    try:
        firebase_admin.initialize_app()
        db = firestore.client()

        if not db.collection("_internal_status").get():
            db.collection("_internal_status").add({"status": "online"}, "health_check")
            print("🟢 CRIADO: coleção `_internal_status` e documento `health_check`")
        else:
            print(
                "🟡 JÁ EXISTEM: coleção `_internal_status` e documento `health_check`"
            )

        print("🔥 Firebase INICIALIZADO com sucesso!")
    except Exception as error:
        print(error)
        raise Exception("❌ NÃO FOI POSSÍVEL inicializar o Firebase nesta aplicação!")


def check_status() -> str | None:
    try:
        db = firestore.client()
        doc_ref = db.collection("_internal_status").document("health_check")
        doc_ref.get()

        return "Online"
    except Exception as error:
        print(error)
        return "Offline"
