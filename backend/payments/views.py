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
        if settings.STRIPE_VERIFY_WEBHOOK_SIGNATURE:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET,
            )
        else:
            event = json.loads(payload)

    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest()

    event_id = event.get("id")
    event_type = event.get("type")

    if not event_id or not event_type:
        return HttpResponseBadRequest()

    # 🔐 Idempotency guard
    if StripeEvent.objects.filter(event_id=event_id).exists():
        return HttpResponse(status=200)

    # Persist event atomically
    with transaction.atomic():
        StripeEvent.objects.create(
            event_id=event_id,
            event_type=event_type,
        )

        if event_type == "payment_intent.succeeded":
            intent = event["data"]["object"]
            order_id = intent.get("metadata", {}).get("order_id")

            if not order_id:
                return HttpResponseBadRequest()

            try:
                order = Order.objects.select_for_update().get(id=order_id)
            except Order.DoesNotExist:
                return HttpResponseBadRequest()

            # ✅ State-safe update
            if order.status != Order.STATUS_PAID:
                order.status = Order.STATUS_PAID
                order.payment_intent_id = intent["id"]
                order.save(update_fields=["status", "payment_intent_id"])

    return HttpResponse(status=200)
