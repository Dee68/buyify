import pytest # type: ignore
from orders.models import Order
from django.contrib.auth import get_user_model # type: ignore

User = get_user_model()

@pytest.fixture
def paid_order(db):
    # Create a test user
    user = User.objects.create_user(email="test@example.com", password="password123")

    # Create a paid order
    order = Order.objects.create(
        user=user,
        status=Order.STATUS_PAID,
        payment_intent_id="pi_test_paid_123",
        total_price=2500
    )
    return order
