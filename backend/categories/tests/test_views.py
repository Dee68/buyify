import pytest # type: ignore
from django.urls import reverse # type: ignore
from categories.models import Category


@pytest.mark.django_db
def test_list_categories(client):
    Category.objects.create(name="Electronics")
    Category.objects.create(name="Books")

    url = reverse("categories:categories-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2



@pytest.mark.django_db
def test_retrieve_category(client):
    category = Category.objects.create(name="Furniture")

    url = reverse("categories:categories-detail", args=[category.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == "Furniture"
