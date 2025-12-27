from models import user
from faker import Faker

fake = Faker()


def create_user(username: str = None, email: str = None, password: str = None):
    new_user = user.create(
        username=username or fake.name(),
        email=email or fake.email(),
        password=password or "validpassword",
    )

    return new_user
