import pytest # type: ignore
from django.urls import reverse # type: ignore
from django.utils import timezone # type: ignore
from datetime import timedelta
from rest_framework.test import APIClient # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken # type: ignore

@pytest.mark.django_db
def test_token_refresh_success(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="refresh@test.com",
        password="testpass123",
    )

    refresh = RefreshToken.for_user(user)

    url = reverse("users:token_refresh")
    response = client.post(url, {
        "refresh": str(refresh)
    })

    assert response.status_code == 200
    assert "access" in response.data

@pytest.mark.django_db
def test_token_refresh_invalid_token(client):
    url = reverse("users:token_refresh")
    response = client.post(url, {
        "refresh": "this.is.not.a.valid.token"
    })

    assert response.status_code == 401

@pytest.mark.django_db
def test_expired_access_token_rejected(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="expired@test.com",
        password="testpass123",
    )

    token = AccessToken.for_user(user)
    token.set_exp(from_time=timezone.now() - timedelta(minutes=10))
    client = APIClient()

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {str(token)}"
    )

    url = reverse("users:profile")
    response = client.get(url)

    assert response.status_code == 401

@pytest.mark.django_db
def test_refresh_token_allows_access_to_protected_view(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="flow@test.com",
        password="testpass123",
    )

    refresh = RefreshToken.for_user(user)

    refresh_url = reverse("users:token_refresh")
    refresh_response = client.post(refresh_url, {
        "refresh": str(refresh)
    })

    access = refresh_response.data["access"]

    client = APIClient()

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )

    profile_url = reverse("users:profile")
    response = client.get(profile_url)

    assert response.status_code == 200
    assert response.data["email"] == user.email


