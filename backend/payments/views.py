import json
import stripe # type: ignore
from django.conf import settings # type: ignore
from django.http import HttpResponse, HttpResponseBadRequest # type: ignore
from django.db import transaction # type: ignore

from orders.models import Order
from payments.models import StripeEvent


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        if getattr(settings, "STRIPE_VERIFY_WEBHOOK_SIGNATURE", True):
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        else:
            event = json.loads(payload)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest()

    data_object = event.get("data", {}).get("object")
    if not data_object:
        return HttpResponseBadRequest()

    # Handle payment_intent.succeeded
    if event["type"] == "payment_intent.succeeded":
        order_id = data_object.get("metadata", {}).get("order_id")
        if not order_id:
            return HttpResponseBadRequest()

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponseBadRequest()

        order.payment_intent_id = data_object["id"]
        order.status = Order.STATUS_PAID
        order.save(update_fields=["payment_intent_id", "status"])

    # Handle refunds
    elif event["type"] == "charge.refunded":
        try:
            order = Order.objects.get(payment_intent_id=data_object.get("payment_intent"))
        except Order.DoesNotExist:
            return HttpResponseBadRequest()

        order.status = Order.STATUS_REFUNDED
        order.refund_id = data_object["refunds"]["data"][0]["id"]
        order.save(update_fields=["status", "refund_id"])

    # Handle disputes
    elif event["type"] == "charge.dispute.created":
        try:
            order = Order.objects.get(payment_intent_id=data_object.get("payment_intent"))
        except Order.DoesNotExist:
            return HttpResponseBadRequest()

        order.status = Order.STATUS_DISPUTED
        order.save(update_fields=["status"])

    return HttpResponse(status=200)
