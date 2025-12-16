import pytest # type: ignore
from products.models import ProductVariant


@pytest.mark.django_db
def test_product_price_resolves_from_variants(product):
    ProductVariant.objects.create(
        product=product,
        sku="SKU-LOW",
        price=50,
        stock=5,
        is_active=True,
    )
    ProductVariant.objects.create(
        product=product,
        sku="SKU-HIGH",
        price=100,
        stock=5,
        is_active=True,
    )

    assert product.resolved_price == 50

@pytest.mark.django_db
def test_product_stock_aggregates_variants(product):
    ProductVariant.objects.create(
        product=product,
        sku="SKU-1",
        price=50,
        stock=3,
        is_active=True,
    )
    ProductVariant.objects.create(
        product=product,
        sku="SKU-2",
        price=60,
        stock=7,
        is_active=True,
    )

    assert product.resolved_stock == 10

@pytest.mark.django_db
def test_inactive_variants_are_ignored(product):
    ProductVariant.objects.create(
        product=product,
        sku="ACTIVE",
        price=80,
        stock=4,
        is_active=True,
    )
    ProductVariant.objects.create(
        product=product,
        sku="INACTIVE",
        price=10,
        stock=100,
        is_active=False,
    )

    assert product.resolved_price == 80
    assert product.resolved_stock == 4
