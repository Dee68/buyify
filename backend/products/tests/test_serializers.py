import pytest # type: ignore
from products.serializers import ProductSerializer


@pytest.fixture
def valid_product_data():
    return {
        "name": "Test Product",
        "description": "Nice item",
        "price": "10.00",
        "stock": 5,
    }

@pytest.mark.django_db
def test_product_serializer_valid_data(valid_product_data):
    serializer = ProductSerializer(data=valid_product_data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_product_serializer_negative_price(valid_product_data):
    valid_product_data["price"] = "-5.00"

    serializer = ProductSerializer(data=valid_product_data)

    assert not serializer.is_valid()
    assert "price" in serializer.errors

@pytest.mark.django_db
def test_product_serializer_negative_stock(valid_product_data):
    valid_product_data["stock"] = -1

    serializer = ProductSerializer(data=valid_product_data)

    assert not serializer.is_valid()
    assert "stock" in serializer.errors

@pytest.mark.django_db
def test_product_serializer_empty_name(valid_product_data):
    valid_product_data["name"] = "   "

    serializer = ProductSerializer(data=valid_product_data)

    assert not serializer.is_valid()
    assert "name" in serializer.errors
