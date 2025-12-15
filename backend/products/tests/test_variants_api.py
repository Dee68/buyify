import pytest # type: ignore
from products.models import (
    ProductVariant,
)

@pytest.mark.django_db
def test_product_returns_variants(api_client, product):
    ProductVariant.objects.create(
        product=product,
        sku="SKU-1",
        price=9.99,
        stock=3,
    )

    response = api_client.get(f"/api/products/{product.id}/")

    assert response.status_code == 200
    assert len(response.data["variants"]) == 1
