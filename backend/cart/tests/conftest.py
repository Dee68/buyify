import pytest # type: ignore
from cart.models import Cart, CartItem
from products.models import ProductVariant


@pytest.fixture
def variant(product):
    return ProductVariant.objects.create(
        product=product,
        sku="TEST-SKU",
        price=product.price,
        stock=10,
        is_active=True,
    )


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_item(cart, variant):
    return CartItem.objects.create(
        cart=cart,
        variant=variant,
        quantity=1,
    )


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(
        email="other@test.com",
        password="password123",
    )
