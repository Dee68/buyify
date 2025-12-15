import pytest  # type: ignore
from categories.models import Category
from products.models import Product
from django.db import IntegrityError # type: ignore
from django.db.models.deletion import ProtectedError # type: ignore
from rest_framework.test import APIClient # type: ignore


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Electronics")

    assert category.name == "Electronics"
    assert category.slug == "electronics"
    assert category.created_at is not None


@pytest.mark.django_db
def test_category_str_representation():
    category = Category.objects.create(name="Books")
    assert str(category) == "Books"

@pytest.mark.django_db
def test_category_name_must_be_unique():
    Category.objects.create(name="Fashion")

    with pytest.raises(IntegrityError):
        Category.objects.create(name="Fashion")

@pytest.mark.django_db
def test_cannot_delete_category_with_products():
    category = Category.objects.create(name="Electronics")
    Product.objects.create(
        name="Laptop",
        price=1000,
        stock=5,
        category=category,
    )

    with pytest.raises(ProtectedError):
        category.delete()

@pytest.mark.django_db
def test_category_hierarchy():
    parent = Category.objects.create(name="Electronics")
    child = Category.objects.create(name="Phones", parent=parent)

    assert child.parent == parent
    assert parent.children.count() == 1

@pytest.mark.django_db
def test_category_product_count(category, product_factory):
    product_factory(category=category)
    product_factory(category=category)

    client = APIClient()

    response = client.get("/api/categories/") 
    assert response.status_code == 200
    assert response.data["results"][0]["product_count"] == 2
