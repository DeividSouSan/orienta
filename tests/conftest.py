from time import sleep
from dotenv import load_dotenv
import pytest
from firebase_admin.auth import ListUsersPage
from firebase_admin import auth
import firebase_admin

from src.models import user

load_dotenv()

ACCOUNTS_BATCH_SIZE = 100  # máximo permitido pelo Firebase
GUIDES_BATCH_SIZE = 100
DELAY_SECONDS = 0.5  # espera entre lotes para evitar rate limit


@pytest.fixture(scope="session", autouse=True)
def initialize_firebase_app():
    app = firebase_admin.initialize_app()

    print("🟢 🔥 Firebase inicializado com sucesso no inicio da sessão")

    yield app

    firebase_admin.delete_app(app)

    print("\n🟥 🔥 Firebase desconectado no final da sessão")


@pytest.fixture(scope="session", autouse=True)
def clear_firebase_auth(initialize_firebase_app):
    print("🧹 Limpando usuários do Firebase Auth...")

    users: ListUsersPage = auth.list_users()
    batch = []

    for user_account in users.iterate_all():
        batch.append(user_account.uid)

        if len(batch) == ACCOUNTS_BATCH_SIZE:
            auth.delete_users(batch)
            print(f"  - Removidos {len(batch)} usuários")
            batch.clear()
            sleep(DELAY_SECONDS)

    if batch:
        auth.delete_users(batch)
        print(f"  - Removidos {len(batch)} usuários (último lote)")

    print("✅ Limpeza concluída.")


@pytest.fixture(scope="session", autouse=True)
def clear_study_guides_collection(initialize_firebase_app):
    from firebase_admin import firestore

    print("🧹 Limpando a coleção 'study_guides' do Firestore...")

    db = firestore.client()
    guides_collection_ref = db.collection("study_guides")
    batch = []

    for guide in guides_collection_ref.list_documents():
        batch.append(guide.id)
        guide.delete()

        if len(batch) == GUIDES_BATCH_SIZE:
            print(f"  - Removidos {len(batch)} usuários")
            batch.clear()
            sleep(DELAY_SECONDS)

    print("✅ Limpeza concluída.")


@pytest.fixture(scope="session", autouse=True)
def add_mock_user(
    initialize_firebase_app, clear_firebase_auth, clear_study_guides_collection
):
    print("👤 Adicionando usuário mock ao Firebase Auth...")

    user.create(
        username="mock",
        email="mock@orienta.com",
        password="123456",
    )

    print("✅ Usuário criado com sucesso..")
