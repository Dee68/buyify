import pytest # type: ignore
from products.serializers import ProductSerializer,ProductWriteSerializer
from products.models import Product
from categories.models import Category


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

    serializer = ProductWriteSerializer(data=valid_product_data)

    assert not serializer.is_valid()
    assert "price" in serializer.errors

@pytest.mark.django_db
def test_product_serializer_negative_stock(valid_product_data):
    valid_product_data["stock"] = -1

    serializer = ProductWriteSerializer(data=valid_product_data)

    assert not serializer.is_valid()
    assert "stock" in serializer.errors

@pytest.mark.django_db
def test_product_serializer_empty_name(valid_product_data):
    valid_product_data["name"] = "   "

    serializer = ProductSerializer(data=valid_product_data)

    assert not serializer.is_valid()
    assert "name" in serializer.errors



@pytest.mark.django_db
def test_product_serializer_accepts_category_id(valid_product_data):
    category = Category.objects.create(name="Books")
    valid_product_data["category"] = category.id

    serializer = ProductWriteSerializer(data=valid_product_data)
    assert serializer.is_valid(), serializer.errors

    product = serializer.save()
    assert product.category == category

@pytest.mark.django_db
def test_product_serializer_invalid_category_id(valid_product_data):
    valid_product_data["category"] = 9999

    serializer = ProductSerializer(data=valid_product_data)
    assert not serializer.is_valid()
    assert "category" in serializer.errors


@pytest.mark.django_db
def test_product_serializer_returns_category_detail():
    category = Category.objects.create(name="Furniture")

    product = Product.objects.create(
        name="Chair",
        description="Wooden chair",
        price=50,
        stock=10,
        category=category,
    )

    serializer = ProductSerializer(product)
    data = serializer.data

    assert data["category"] == category.id
    assert data["category_detail"]["name"] == "Furniture"


