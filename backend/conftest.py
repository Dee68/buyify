import pytest # type: ignore
import uuid
from django.contrib.auth import get_user_model # type: ignore
from rest_framework.test import APIClient # type: ignore
from categories.models import Category
from products.models import Product

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
def admin_user(db):
    return User.objects.create_superuser(email="admin@test.com", password="adminpass")

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def disable_throttling(settings):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
