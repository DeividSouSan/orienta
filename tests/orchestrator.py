import random

from faker import Faker
from firebase_admin import firestore

from dtos.guide_request import GuideRequest
from dtos.session_create import SessionCreateDTO
from dtos.user_create_request import UserCreateRequest
from models import auth, guide, session, user
from objects.email import Email
from objects.guide_id import GuideId
from objects.password import Password
from objects.username import Username

fake = Faker()


def create_user(username: str = None, email: str = None, password: str = None):
    request = UserCreateRequest(
        username=Username(username or fake.name()),
        email=Email(email or fake.email()),
        password=Password(password or "validpassword"),
    )

    new_user = user.create(request)

    return new_user


def authenticate(email: str, password: str):
    auth_user = auth.authenticate(Email(email), Password(password))
    session_create_data = SessionCreateDTO.from_auth_response(auth_user)
    session_cookie = session.create(session_create_data)

    return session_cookie


def create_guide(owner: str | None = None, days: int | None = None):
    owner = owner or fake.user_name()
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
        owner=Username(owner),
        inputs=guide_request,
    )

    guide_from_db = guide.save(new_guide)

    return guide_from_db


def delete_guide(guide_id: str, username: str):
    guide.delete(GuideId(guide_id), Username(username))


def clear_database():
    GUIDES_BATCH_SIZE = 100

    db = firestore.client()
    guides_collection_ref = db.collection("users_guides")
    batch = []

    for guide_ref in guides_collection_ref.list_documents():
        batch.append(guide_ref.id)
        guide_ref.delete()

        if len(batch) == GUIDES_BATCH_SIZE:
            print(f"  - Removidos {len(batch)} guias.")
            batch.clear()
