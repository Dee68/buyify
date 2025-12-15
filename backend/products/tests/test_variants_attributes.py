import pytest # type: ignore
from products.models import (
    ProductVariant,
    VariantAttribute,
    VariantAttributeValue,
    VariantValueAssignment,
)

@pytest.mark.django_db
def test_variant_attributes_assignment(product):
    variant = ProductVariant.objects.create(
        product=product,
        sku="SKU-BLUE-L",
        price=29.99,
        stock=5,
    )

    color = VariantAttribute.objects.create(name="Color")
    blue = VariantAttributeValue.objects.create(attribute=color, value="Blue")

    VariantValueAssignment.objects.create(
        variant=variant,
        attribute_value=blue,
    )

    assert variant.attribute_values.count() == 1
