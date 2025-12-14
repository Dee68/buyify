import pytest # type: ignore
from django.urls import reverse # type: ignore

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
