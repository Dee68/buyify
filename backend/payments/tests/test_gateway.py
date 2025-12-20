import pytest # type: ignore
from unittest.mock import patch
from orders.models import Order
from payments.gateway import StripeGateway

@pytest.mark.django_db
def test_create_payment_intent(order_factory):
    order = order_factory()
    amount_cents = int(order.total_price * 100)

    with patch("stripe.PaymentIntent.create") as mock_create:
        mock_create.return_value.id = "pi_123"
        mock_create.return_value.client_secret = "secret_123"
        intent = StripeGateway.create_payment_intent(amount=amount_cents, metadata={"order_id": order.id})
        assert intent.client_secret == "secret_123"

@pytest.mark.django_db
def test_mark_paid_updates_order(order_factory):
    order = order_factory(status=Order.STATUS_PENDING)
    order.mark_paid("pi_123")
    assert order.status == Order.STATUS_PAID
    assert order.payment_intent_id == "pi_123"
    assert order.paid_at is not None
