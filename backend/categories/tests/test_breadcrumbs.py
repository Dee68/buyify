import pytest # type: ignore
from categories.models import Category
from rest_framework.test import APIClient # type: ignore


@pytest.mark.django_db
def test_category_breadcrumbs_root_category():
    category = Category.objects.create(
        name="Electronics",
        slug="electronics",
    )

    client = APIClient()
    response = client.get("/api/categories/")

    assert response.status_code == 200
    assert response.data["results"][0]["breadcrumbs"] == [
        {
            "id": category.id,
            "name": "Electronics",
            "slug": "electronics",
        }
    ]

@pytest.mark.django_db
def test_category_breadcrumbs_nested_category():
    root = Category.objects.create(
        name="Electronics",
        slug="electronics",
    )
    child = Category.objects.create(
        name="Laptops",
        slug="laptops",
        parent=root,
    )
    grandchild = Category.objects.create(
        name="Gaming Laptops",
        slug="gaming-laptops",
        parent=child,
    )

    client = APIClient()
    response = client.get("/api/categories/")

    assert response.status_code == 200

    breadcrumbs = next(
        item["breadcrumbs"]
        for item in response.data["results"]
        if item["id"] == grandchild.id
    )

    assert breadcrumbs == [
        {"id": root.id, "name": "Electronics", "slug": "electronics"},
        {"id": child.id, "name": "Laptops", "slug": "laptops"},
        {"id": grandchild.id, "name": "Gaming Laptops", "slug": "gaming-laptops"},
    ]

@pytest.mark.django_db
def test_get_breadcrumbs_model_method():
    root = Category.objects.create(name="Electronics", slug="electronics")
    child = Category.objects.create(name="Laptops", slug="laptops", parent=root)

    breadcrumbs = child.get_breadcrumbs()

    assert breadcrumbs == [
        {"id": root.id, "name": "Electronics", "slug": "electronics"},
        {"id": child.id, "name": "Laptops", "slug": "laptops"},
    ]
