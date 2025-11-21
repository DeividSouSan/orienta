from time import sleep
from dotenv import load_dotenv
import pytest
from firebase_admin.auth import ListUsersPage
from firebase_admin import auth as fireauth
from firebase_admin import firestore

import firebase_admin
import requests

from src.models import user, guide, auth, session

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

    users: ListUsersPage = fireauth.list_users()
    batch = []

    for user_account in users.iterate_all():
        batch.append(user_account.uid)

        if len(batch) == ACCOUNTS_BATCH_SIZE:
            fireauth.delete_users(batch)
            print(f"  - Removidos {len(batch)} usuários.")
            batch.clear()
            sleep(DELAY_SECONDS)

    if batch:
        fireauth.delete_users(batch)
        print(f"  - Removidos {len(batch)} usuários (último lote).")

    print("✅ Limpeza concluída.")


@pytest.fixture(scope="module", autouse=True)
def clear_users_guides_collection(initialize_firebase_app):
    print("🧹 Limpando a coleção 'users_guides' do Firestore...")

    db = firestore.client()
    guides_collection_ref = db.collection("users_guides")
    batch = []

    for guide_ref in guides_collection_ref.list_documents():
        batch.append(guide_ref.id)
        guide_ref.delete()

        if len(batch) == GUIDES_BATCH_SIZE:
            print(f"  - Removidos {len(batch)} guias.")
            batch.clear()
            sleep(DELAY_SECONDS)

    print("✅ Limpeza concluída.")


@pytest.fixture(scope="session", autouse=True)
def clear_users_collection(initialize_firebase_app):
    print("🧹 Limpando a coleção 'users' do Firestore...")

    db = firestore.client()
    users_collection_ref = db.collection("users")
    batch = []

    for user_ref in users_collection_ref.list_documents():
        batch.append(user_ref.id)
        user_ref.delete()

        if len(batch) == ACCOUNTS_BATCH_SIZE:
            print(f"  - Removidos {len(batch)} usuários")
            batch.clear()
            sleep(DELAY_SECONDS)

    print("✅ Limpeza concluída.")


@pytest.fixture(scope="session", autouse=True)
def add_mock_user_and_guides(
    initialize_firebase_app, clear_firebase_auth, clear_users_collection
):
    print("👤 Adicionando usuário mock ao Firebase Auth...")

    user.create(
        username="mock",
        email="mock@orienta.com",
        password="123456",
    )

    guide1 = guide.generate_with_metadata(
        owner="test",
        title="Guia do Test 1",
        is_public=True,
        inputs={
            "topic": "Eu quero entender o que são os workers que eu tenho que configurar no gunicorn.",
            "focus_time": 60,
            "days": 3,
            "knowledge": "zero",
        },
    )

    guide2 = guide.generate_with_metadata(
        owner="test",
        title="Guia do Test 2",
        is_public=False,
        inputs={
            "topic": "Quero compreender como o cérebro humano é capaz de gerar sua própria eletricidade.",
            "focus_time": 30,
            "days": 3,
            "knowledge": "iniciante",
        },
    )

    guide.save(guide1)
    guide.save(guide2)

    print("✅ Usuário criado com sucesso..")


@pytest.fixture(scope="module")
def mock_session(clear_users_guides_collection):
    print("\n🍪 Criando sessão e adicionando cookie...")
    sess = requests.Session()

    user_data = auth.authenticate("mock@orienta.com", "123456")
    session_cookie = session.create(user_data["idToken"])

    sess.cookies.set("session_id", session_cookie)

    yield sess

    print("\n🧹 Fechando a sessão.\n")
