from models import auth, session, user
from faker import Faker

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
