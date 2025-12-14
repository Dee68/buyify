import pytest # type: ignore
from django.contrib.auth import get_user_model # type: ignore

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@test.com", password="pass123")

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(email="admin@test.com", password="adminpass")
