import pytest # type: ignore
from django.urls import reverse # type: ignore
from products.models import Product
from categories.models import Category
from rest_framework.test import APIClient # type: ignore
#from rest_framework_simplejwt.tokens import RefreshToken # type: ignore


# =======================
# Search Tests
# =======================

@pytest.mark.django_db
def test_product_search_by_name(client):
    Product.objects.create(name="Apple iPhone", description="Phone", price=1000, stock=5)
    Product.objects.create(name="Samsung TV", description="Television", price=500, stock=3)

    url = reverse("products:products-list")
    response = client.get(url, {"search": "iphone"})

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert "iPhone" in response.data["results"][0]["name"]

@pytest.mark.django_db
def test_product_search_by_description(client):
    Product.objects.create(name="Laptop", description="Powerful machine", price=1200, stock=4)
    Product.objects.create(name="Mouse", description="Accessory", price=25, stock=10)

    url = reverse("products:products-list")
    response = client.get(url, {"search": "powerful"})

    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Laptop"

# ==============================
# Ordering Tests
# ==============================

@pytest.mark.django_db
def test_product_ordering_by_price(client):
    Product.objects.create(name="Cheap", price=5, stock=1)
    Product.objects.create(name="Expensive", price=100, stock=1)

    url = reverse("products:products-list")
    response = client.get(url, {"ordering": "price"})

    results = response.data["results"]
    assert results[0]["price"] == "5.00"
    assert results[1]["price"] == "100.00"

@pytest.mark.django_db
def test_product_ordering_by_price_desc(client):
    Product.objects.create(name="Cheap", price=5, stock=1)
    Product.objects.create(name="Expensive", price=100, stock=1)

    url = reverse("products:products-list")
    response = client.get(url, {"ordering": "-price"})

    results = response.data["results"]
    assert results[0]["price"] == "100.00"

# ==========================
# 
# ==========================
@pytest.mark.django_db
def test_filter_products_by_category():
    client = APIClient()

    electronics = Category.objects.create(name="Electronics")
    books = Category.objects.create(name="Books")

    Product.objects.create(
        name="Laptop",
        description="Gaming",
        price=1000,
        stock=3,
        category=electronics,
    )
    Product.objects.create(
        name="Novel",
        description="Fiction",
        price=20,
        stock=10,
        category=books,
    )

    response = client.get("/api/products/", {"category": electronics.id})

    assert response.status_code == 200
    assert response.data["count"] == 1

