import pytest # type: ignore
from products.models import Product

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
