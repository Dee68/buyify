import pytest # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from rest_framework.test import APIClient # type: ignore

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@test.com", password="pass123")

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(email="admin@test.com", password="adminpass")

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def disable_throttling(settings):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
