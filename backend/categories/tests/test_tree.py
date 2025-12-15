import pytest # type: ignore
from rest_framework.test import APIClient # type: ignore
from categories.models import Category


@pytest.mark.django_db
def test_category_tree_endpoint():
    root = Category.objects.create(name="Electronics", slug="electronics")
    child = Category.objects.create(name="Laptops", slug="laptops", parent=root)
    leaf = Category.objects.create(name="Gaming", slug="gaming", parent=child)

    client = APIClient()
    response = client.get("/api/categories/tree/")

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["name"] == "Electronics"
    assert response.data[0]["children"][0]["name"] == "Laptops"
    assert response.data[0]["children"][0]["children"][0]["name"] == "Gaming"

@pytest.mark.django_db
def test_category_tree_not_paginated():
    Category.objects.create(name="Electronics", slug="electronics")

    client = APIClient()
    response = client.get("/api/categories/tree/")

    assert isinstance(response.data, list)
