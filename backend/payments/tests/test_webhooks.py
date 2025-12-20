import json
import stripe # type: ignore
import pytest # type: ignore
from django.urls import reverse
from orders.models import Order


@pytest.mark.django_db
def test_webhook_payment_intent_succeeded(
    client, order_factory, settings, mocker
):
    order = order_factory(status=Order.STATUS_PENDING)

    payload = {
        "id": "evt_test_123",
        "type": "payment_intent.succeeded",
        "data": {
            "object": {
                "id": "pi_test_123",
                "metadata": {
                    "order_id": str(order.id)
                }
            }
        }
    }

    mocker.patch(
        "stripe.Webhook.construct_event",
        return_value=payload
    )

    response = client.post(
        reverse("stripe-webhook"),
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test",
    )

    order.refresh_from_db()

    assert response.status_code == 200
    assert order.status == Order.STATUS_PAID
    assert order.payment_intent_id == "pi_test_123"

@pytest.mark.django_db
def test_webhook_invalid_signature(client, mocker):
    mocker.patch(
        "stripe.Webhook.construct_event",
        side_effect=stripe.error.SignatureVerificationError(
            "Invalid signature", sig_header="bad"
        )
    )

    response = client.post(
        reverse("stripe-webhook"),
        data="{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="bad",
    )

    assert response.status_code == 400
