import stripe  # type: ignore
from django.conf import settings # type: ignore
from django.http import HttpResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_POST # type: ignore
#from django.db import transaction

from orders.models import Order


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    except ValueError:
        return HttpResponse(status=400)

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "payment_intent.succeeded":
        _handle_payment_intent_succeeded(data)

    elif event_type == "payment_intent.payment_failed":
        _handle_payment_intent_failed(data)

    elif event_type == "charge.dispute.created":
        dispute = event["data"]["object"]
        payment_intent_id = dispute.get("payment_intent")

        try:
            order = Order.objects.select_for_update().get(
                payment_intent_id=payment_intent_id
            )
        except Order.DoesNotExist:
            return HttpResponse(status=400)

        order.status = Order.STATUS_DISPUTED
        order.save(update_fields=["status"])


    elif event_type == "charge.refunded":
        charge = event["data"]["object"]
        payment_intent_id = charge.get("payment_intent")

    try:
        order = Order.objects.select_for_update().get(
            payment_intent_id=payment_intent_id
        )
    except Order.DoesNotExist:
        return HttpResponse(status=400)

    order.status = Order.STATUS_REFUNDED
    order.refund_id = charge["refunds"]["data"][0]["id"]
    order.save(update_fields=["status", "refund_id"])


    return HttpResponse(status=200)


def _handle_payment_intent_succeeded(intent):
    order_id = intent["metadata"].get("order_id")
    if not order_id:
        return

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    order.mark_paid(payment_intent_id=intent["id"])


def _handle_payment_intent_failed(intent):
    order_id = intent["metadata"].get("order_id")
    if not order_id:
        return

    Order.objects.filter(id=order_id).update(status=Order.STATUS_FAILED)