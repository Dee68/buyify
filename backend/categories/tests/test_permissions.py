import pytest

@pytest.mark.django_db
def test_non_admin_cannot_create_category(api_client, user):
    api_client.force_authenticate(user=user)

    response = api_client.post("/api/categories/", {"name": "Electronics"})
    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_can_create_category(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post("/api/categories/", {"name": "Electronics"})
    assert response.status_code == 201
