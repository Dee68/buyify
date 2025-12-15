import pytest # type: ignore
from products.models import (
    ProductVariant,
)


@pytest.mark.django_db
def test_create_product_variant(product):
    variant = ProductVariant.objects.create(
        product=product,
        sku="SKU-RED-M",
        price=19.99,
        stock=10,
    )

    assert variant.product == product
    assert variant.sku == "SKU-RED-M"
