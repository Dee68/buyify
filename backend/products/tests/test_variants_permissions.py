import pytest # type: ignore
from rest_framework import status # type: ignore
from rest_framework.test import APIClient # type: ignore


@pytest.mark.django_db
def test_non_admin_cannot_create_variant(product, user):
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/products/variants/",
        {
            "product": product.id,
            "sku": "FORBIDDEN",
            "price": 99,
            "stock": 5,
            "is_active": True,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_anonymous_cannot_create_variant(product):
    client = APIClient()

    response = client.post(
        "/api/products/variants/",
        {
            "product": product.id,
            "sku": "ANON",
            "price": 99,
            "stock": 5,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
