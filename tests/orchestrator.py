import random
from time import sleep

from faker import Faker
from firebase_admin import firestore

from dtos.guide_request import GuideRequest
from models import auth, guide, session, user

fake = Faker()


def create_user(username: str = None, email: str = None, password: str = None):
    new_user = user.create(
        username=username or fake.name(),
        email=email or fake.email(),
        password=password or "validpassword",
    )

    return new_user


def authenticate(email: str, password: str):
    auth_user = auth.authenticate(email, password)
    session_cookie = session.create(token=auth_user["idToken"])

    return session_cookie


def create_guide(owner: str | None = None, days: int | None = None):
    guide_request = GuideRequest.from_dict(
        {
            "title": "Título Teste",
            "topic": "Eu quero estudar sobre docker. Como funciona e quais são seus principais comandos.",
            "knowledge": "zero",
            "focus_time": random.choice([30, 60, 120]),
            "days": days or random.randint(3, 30),
        }
    )

    new_guide = guide.generate_with_metadata(
        owner=owner,
        inputs=guide_request,
    )

    guide_from_db = guide.save(new_guide)

    return guide_from_db


def delete_guide(guide_id: str, username: str):
    guide.delete(guide_id, username)


def clear_database():
    GUIDES_BATCH_SIZE = 100
    DELAY_SECONDS = 0.5

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
