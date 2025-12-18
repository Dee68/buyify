import pytest # type: ignore
from rest_framework import status # type: ignore

pytestmark = pytest.mark.django_db


def test_user_can_checkout_cart(api_client, user, product_variant):
    api_client.force_authenticate(user=user)

    # Add item to cart
    api_client.post(
        "/api/items/",
        {"variant": product_variant.id, "quantity": 2},
    )

    response = api_client.post("/api/orders/")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["total_price"] == str(
        product_variant.price * 2
    )
    assert len(response.data["items"]) == 1

def test_cart_is_cleared_after_checkout(api_client, user, product_variant):
    api_client.force_authenticate(user=user)

    api_client.post(
        "/api/items/",
        {"variant": product_variant.id, "quantity": 1},
    )

    api_client.post("/api/orders/")

    cart_response = api_client.get("/api/cart/")
    assert cart_response.data["items"] == []


def test_cannot_checkout_empty_cart(api_client, user):
    api_client.force_authenticate(user=user)

    response = api_client.post("/api/orders/")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "empty" in response.data["detail"].lower()

def test_anonymous_user_cannot_checkout(api_client):
    response = api_client.post("/api/orders/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_order_price_is_frozen(api_client, user, product_variant):
    api_client.force_authenticate(user=user)

    api_client.post(
        "/api/items/",
        {"variant": product_variant.id, "quantity": 1},
    )

    response = api_client.post("/api/orders/")
    order_price = response.data["total_price"]

    # Change variant price AFTER order
    product_variant.price += 50
    product_variant.save()

    order_response = api_client.get(
        f"/api/orders/{response.data['id']}/"
    )

    assert order_response.data["total_price"] == order_price
