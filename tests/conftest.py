from time import sleep
from dotenv import load_dotenv
import pytest
from firebase_admin.auth import ListUsersPage
from firebase_admin import auth as fireauth
from firebase_admin import firestore

import requests

from tests import orchestrator
from main import app as flask_app

load_dotenv()

ACCOUNTS_BATCH_SIZE = 100  # máximo permitido pelo Firebase
GUIDES_BATCH_SIZE = 100
DELAY_SECONDS = 0.5  # espera entre lotes para evitar rate limit


@pytest.fixture(scope="session", autouse=True)
def clear_firebase_auth():
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
def clear_users_guides_collection():
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
def clear_users_collection():
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


@pytest.fixture(scope="module")
def auth_request():
    sess = requests.Session()

    new_user = orchestrator.create_user()
    session_cookie = orchestrator.authenticate(new_user["email"], "validpassword")
    sess.cookies.set("session_id", session_cookie)

    yield sess


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "ignore_localhost": True,
        "decode_compressed_response": True,
        "filter_headers": [("x-goog-api-key", "XD")],
        "filter_query_parameters": ["key"],
        "ignore_hosts": [
            "oauth2.googleapis.com",  # Autenticação Google/Firebase
            "accounts.google.com",  # Autenticação Google
            "identitytoolkit.googleapis.com",  # Firebase Auth
            "firestore.googleapis.com",  # Firestore Database
            "securetoken.googleapis.com",
            "www.googleapis.com",
        ],
    }


@pytest.fixture(scope="session")
def new_user():
    return orchestrator.create_user()


@pytest.fixture(scope="session")
def session_cookie(new_user):
    return orchestrator.authenticate(new_user["email"], "validpassword")


@pytest.fixture(scope="function")
def client():
    with flask_app.test_client() as request:
        yield request


@pytest.fixture(scope="function")
def auth_client(session_cookie):
    with flask_app.test_client() as auth_request:
        auth_request.set_cookie("session_id", session_cookie)
        yield auth_request
