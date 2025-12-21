from django.db import transaction # type: ignore
from orders.models import Order
from payments.gateway import StripeGateway

def request_refund(order: Order, amount: int | None = None):
    if order.status != Order.STATUS_PAID:
        raise ValueError("Only paid orders can be refunded")

    refund = StripeGateway.create_refund(
        payment_intent_id=order.payment_intent_id,
        amount=amount,
    )

    # Do NOT mark refunded here — wait for webhook
    return refund
