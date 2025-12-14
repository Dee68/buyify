import pytest # type: ignore
from django.urls import reverse # type: ignore
from products.models import Product
from rest_framework.test import APIClient # type: ignore


@pytest.mark.django_db
def test_list_products(client):
    Product.objects.create(name="Item 1", description="A", price=5, stock=3)
    Product.objects.create(name="Item 2", description="B", price=10, stock=5)

    url = reverse("products:products-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_create_product(client, admin_user):
    #client.force_login(admin_user)
    client = APIClient()

    client.force_authenticate(user=admin_user)

    url = reverse("products:products-list")
    response = client.post(url, {
        "name": "New Product",
        "description": "Nice item",
        "price": 25.50,
        "stock": 12
    }, format="json",)

    assert response.status_code == 201
    assert response.data["name"] == "New Product"
