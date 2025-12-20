import pytest # type: ignore
import uuid
from django.contrib.auth import get_user_model # type: ignore
from rest_framework.test import APIClient # type: ignore
from categories.models import Category
from products.models import Product,ProductVariant



@pytest.fixture
def product_variant(product):
    return ProductVariant.objects.create(
        product=product,
        sku="SKU-001",
        price=100,
        stock=10,
        is_active=True,
    )


@pytest.fixture
def order_factory(user):
    from orders.models import Order

    def factory(**kwargs):
        return Order.objects.create(
            user=kwargs.get("user", user),
            total_price=kwargs.get("total_price", 0),
            status=kwargs.get("status", Order.STATUS_PENDING),
        )

    return factory


@pytest.fixture
def product(product_factory, category):
    return product_factory(category=category)

@pytest.fixture
def product_factory():
    def create_product(**kwargs):
        unique_suffix = uuid.uuid4().hex[:8]

        defaults = {
            "name": f"Test Product {unique_suffix}",
            "description": "Test Description",
            "price": 10.00,
            "stock": 5,
        }
        defaults.update(kwargs)
        return Product.objects.create(**defaults)

    return create_product

@pytest.fixture
def category():
    return Category.objects.create(name="Electronics")

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@test.com", password="pass123")

@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email="another@test.com",
        password="password123",
    )

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(email="admin@test.com", password="adminpass")

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def disable_throttling(settings):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
