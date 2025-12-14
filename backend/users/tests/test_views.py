import pytest # type: ignore
from django.urls import reverse # type: ignore
from rest_framework.test import APIClient # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore


# =========================
# Registration Tests
# =========================
@pytest.mark.django_db
def test_user_registration(client):
    url = reverse("users:register")
    response = client.post(url, {
        "email": "test@login.com",
        "password": "StrongPass123!",
        "password2": "StrongPass123!"
    }, format="json",)

    assert response.status_code == 201
    assert "email" in response.data

@pytest.mark.django_db
def test_register_duplicate_email(client, user):
    url = reverse("users:register")
    response = client.post(url, {
        "email": user.email,
        "password": "StrongPass123",
        "password2": "StrongPass123",
    })

    assert response.status_code == 400

@pytest.mark.django_db
def test_register_missing_fields(client):
    url = reverse("users:register")
    response = client.post(url, {
        "email": "",
        "password": "",
        "password2": "",
    })

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_password_mismatch(client):
    url = reverse("users:register")
    response = client.post(url, {
        "email": "mismatch@test.com",
        "password": "password123",
        "password2": "password456",
    })

    assert response.status_code == 400

#==========================
# Login Tests
#==========================

@pytest.mark.django_db
def test_user_login(client, django_user_model):
    django_user_model.objects.create_user(
        email="test@login.com", password="StrongPass123!"
    )

    url = reverse("users:login")
    response = client.post(url, {
        "email": "test@login.com",
        "password": "StrongPass123!"
    },format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_login_wrong_password(client, user):
    url = reverse("users:login")
    response = client.post(url, {
        "email": user.email,
        "password": "wrongpassword",
    })

    assert response.status_code == 401


@pytest.mark.django_db
def test_login_nonexistent_user(client):
    url = reverse("users:login")
    response = client.post(url, {
        "email": "ghost@test.com",
        "password": "doesnotexist",
    })

    assert response.status_code == 401


@pytest.mark.django_db
def test_login_missing_fields(client):
    url = reverse("users:login")
    response = client.post(url, {})

    assert response.status_code == 400

# =========================
# Profile Tests
# =========================

@pytest.mark.django_db
def test_profile_requires_authentication(client):
    url = reverse("users:profile")
    response = client.get(url)

    assert response.status_code == 401

@pytest.mark.django_db
def test_profile_authenticated(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    url = reverse("users:profile")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["email"] == user.email
