import pytest # type: ignore
from products.models import Product
from categories.models import Category
#from django.db import IntegrityError # type: ignore

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


# ===================================
# Category Product relationship Tests
# ===================================

@pytest.mark.django_db
def test_product_can_have_category():
    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        name="Laptop",
        description="Gaming laptop",
        price=1200,
        stock=5,
        category=category,
    )

    assert product.category == category
    assert category.products.count() == 1


