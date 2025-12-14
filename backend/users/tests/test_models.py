import pytest # type: ignore
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="test@example.com",
        password="pass1234"
    )
    assert user.email == "test@example.com"
    assert user.check_password("pass1234")
    assert user.is_active is True

@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        password="admin123"
    )
    assert admin.is_staff is True
    assert admin.is_superuser is True
