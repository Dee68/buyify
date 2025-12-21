import pytest # type: ignore
import json
from unittest.mock import patch
from orders.models import Order
from payments.services import request_refund
from django.urls import reverse # type: ignore

@pytest.mark.django_db
def test_refund_flow(client, paid_order, mocker):
    mocker.patch(
        "stripe.Refund.create",
        return_value={"id": "re_test_123"}
    )

    from payments.services import request_refund

    refund = request_refund(paid_order)

    assert refund["id"] == "re_test_123"
    assert paid_order.status == Order.STATUS_PAID  # not yet updated until webhook

@pytest.mark.django_db
def test_refund_webhook(client, paid_order, mocker):
    payload = {
        "id": "evt_refund_123",
        "type": "charge.refunded",
        "data": {
            "object": {
                "payment_intent": paid_order.payment_intent_id,
                "refunds": {"data": [{"id": "re_test_123"}]},
            }
        }
    }

    mocker.patch("stripe.Webhook.construct_event", return_value=payload)

    response = client.post(
        reverse("stripe-webhook"),
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test",
    )

    paid_order.refresh_from_db()

    assert response.status_code == 200
    assert paid_order.status == Order.STATUS_REFUNDED

@pytest.mark.django_db
def test_chargeback_webhook(client, paid_order, mocker):
    payload = {
        "id": "evt_dispute_123",
        "type": "charge.dispute.created",
        "data": {
            "object": {"payment_intent": paid_order.payment_intent_id}
        }
    }

    mocker.patch("stripe.Webhook.construct_event", return_value=payload)

    response = client.post(
        reverse("stripe-webhook"),
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test",
    )

    paid_order.refresh_from_db()

    assert response.status_code == 200
    assert paid_order.status == Order.STATUS_DISPUTED
