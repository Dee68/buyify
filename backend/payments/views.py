import json
import stripe # type: ignore
from django.conf import settings # type: ignore
from django.http import HttpResponse, HttpResponseBadRequest # type: ignore
from orders.models import Order

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

    # ✅ Defensive guard — REQUIRED
    event_type = event.get("type")
    if not event_type:
        return HttpResponseBadRequest()

    if event_type == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")

        if not order_id:
            return HttpResponseBadRequest()

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponseBadRequest()

        order.status = Order.STATUS_PAID
        order.payment_intent_id = intent["id"]
        order.save(update_fields=["status", "payment_intent_id"])

    return HttpResponse(status=200)
