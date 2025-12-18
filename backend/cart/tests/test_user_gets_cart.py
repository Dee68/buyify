import pytest # type: ignore
from rest_framework import status # type: ignore
from rest_framework.test import APIClient # type: ignore

@pytest.mark.django_db
def test_user_gets_cart_on_first_access(api_client, user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.get("/api/cart/")

    assert response.status_code == 200
    assert response.data["items"] == []

@pytest.mark.django_db
def test_add_variant_to_cart_creates_cart_item(api_client, user, variant):
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.post(
        "/api/cart/items/",
        {
            "variant": variant.id,
            "quantity": 2,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["quantity"] == 2

@pytest.mark.django_db
def test_adding_same_variant_twice_increments_quantity(api_client, user, variant):
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    api_client.post("/api/cart/items/", {"variant": variant.id, "quantity": 1})
    response = api_client.post("/api/cart/items/", {"variant": variant.id, "quantity": 2})

    assert response.status_code == 200
    assert response.data["quantity"] == 3

@pytest.mark.django_db
def test_cannot_add_more_than_available_stock(api_client, user, variant):
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.post(
        "/api/cart/items/",
        {
            "variant": variant.id,
            "quantity": variant.stock + 1,
        },
        format="json",
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_cannot_add_inactive_variant(api_client, user, variant):
    variant.is_active = False
    variant.save()
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.post(
        "/api/cart/items/",
        {
            "variant": variant.id,
            "quantity": 1,
        },
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_update_cart_item_quantity(api_client, user, cart_item):
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        f"/api/cart/items/{cart_item.id}/",
        {"quantity": 3},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["quantity"] == 3

@pytest.mark.django_db
def test_setting_quantity_to_zero_removes_item(api_client, user, cart_item):
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        f"/api/cart/items/{cart_item.id}/",
        {"quantity": 0},
        format="json",
    )

    assert response.status_code == 204


@pytest.mark.django_db
def test_remove_cart_item(api_client, user, cart_item):
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/api/cart/items/{cart_item.id}/")

    assert response.status_code == 204



@pytest.mark.django_db
def test_anonymous_user_cannot_mutate_cart(api_client, variant):
    response = api_client.post(
        "/api/cart/items/",
        {"variant": variant.id, "quantity": 1},
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_user_cannot_modify_other_users_cart(api_client, cart_item, another_user):
    api_client = APIClient()
    api_client.force_authenticate(user=another_user)

    response = api_client.delete(f"/api/cart/items/{cart_item.id}/")

    assert response.status_code == 404

