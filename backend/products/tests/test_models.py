import pytest # type: ignore
from products.models import Product,Category
from django.db import IntegrityError # type: ignore

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(
        name="Test Product",
        description="A sample product",
        price=19.99,
        stock=10
    )
    assert product.name == "Test Product"
    assert product.price == 19.99
    assert product.stock == 10


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


