import pytest # type: ignore
from django.urls import reverse # type: ignore
from products.models import Product
from rest_framework.test import APIClient # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore


@pytest.mark.django_db
def test_list_products(client):
    Product.objects.create(name="Item 1", description="A", price=5, stock=3)
    Product.objects.create(name="Item 2", description="B", price=10, stock=5)

    url = reverse("products:products-list")
    response = client.get(url)

    assert response.status_code == 200
    #assert len(response.data) == 2
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_create_product(client, admin_user):
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

@pytest.mark.django_db
def test_retrieve_product(client):
    product = Product.objects.create(
        name="Test Product",
        description="A product",
        price=19.99,
        stock=5,
    )

    url = reverse("products:products-detail", args=[product.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == "Test Product"
    assert response.data["price"] == "19.99"

@pytest.mark.django_db
def test_update_product_authenticated(client, admin_user):
    product = Product.objects.create(
        name="Old Name",
        description="Old desc",
        price=10.00,
        stock=3,
    )

    client = APIClient()
    client.force_authenticate(user=admin_user)

    url = reverse("products:products-detail", args=[product.id])
    response = client.put(
        url,
        {
            "name": "Updated Name",
            "description": "Updated desc",
            "price": "15.50",
            "stock": 10,
        },
        content_type="application/json",
    )

    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == "Updated Name"
    assert product.price == 15.50
    assert product.stock == 10

@pytest.mark.django_db
def test_update_product_unauthenticated(client):
    product = Product.objects.create(
        name="Readonly",
        description="No edit",
        price=5.00,
        stock=1,
    )

    url = reverse("products:products-detail", args=[product.id])
    response = client.put(
        url,
        {
            "name": "Hacked",
            "description": "Nope",
            "price": "99.99",
            "stock": 99,
        },
        content_type="application/json",
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_delete_product_authenticated(client, admin_user):
    product = Product.objects.create(
        name="Delete Me",
        description="Temp",
        price=8.00,
        stock=2,
    )
    client = APIClient()
    
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    url = reverse("products:products-detail", args=[product.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_delete_product_unauthenticated(client):
    product = Product.objects.create(
        name="Protected",
        description="Cannot delete",
        price=12.00,
        stock=4,
    )
    url = reverse("products:products-detail", args=[product.id])
    response = client.delete(url)

    assert response.status_code == 401

@pytest.mark.django_db
def test_products_list_is_paginated(client):
    for i in range(15):
        Product.objects.create(
            name=f"Product {i}",
            description="Test",
            price=10.00,
            stock=5,
        )

    url = reverse("products:products-list")
    response = client.get(url)

    assert response.status_code == 200
    assert "results" in response.data
    assert "count" in response.data
    assert len(response.data["results"]) == 10
    assert response.data["count"] == 15

@pytest.mark.django_db
def test_products_list_second_page(client):
    for i in range(15):
        Product.objects.create(
            name=f"Product {i}",
            description="Test",
            price=10.00,
            stock=5,
        )

    url = reverse("products:products-list")
    response = client.get(url, {"page": 2})

    assert response.status_code == 200
    assert len(response.data["results"]) == 5
