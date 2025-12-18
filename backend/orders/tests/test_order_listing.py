import pytest # type: ignore
from rest_framework import status # type: ignore

pytestmark = pytest.mark.django_db

def test_user_sees_only_their_orders(api_client, user, another_user, order_factory):
    api_client.force_authenticate(user=user)

    order_factory(user=user)
    order_factory(user=another_user)

    response = api_client.get("/api/orders/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1



def test_order_includes_items_with_unit_price(
    api_client, user, product_variant
):
    api_client.force_authenticate(user=user)

    api_client.post(
        "/api/items/",
        {"variant": product_variant.id, "quantity": 3},
    )

    response = api_client.post("/api/orders/")

    item = response.data["items"][0]
    assert item["quantity"] == 3
    assert item["unit_price"] == str(product_variant.price)

