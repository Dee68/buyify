from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status # type: ignore
from orders.models import Order
from .gateway import stripe
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = getattr(stripe, "WEBHOOK_SECRET", None)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")
        try:
            order = Order.objects.get(id=order_id)
            order.status = Order.STATUS_PAID
            order.save()
        except Order.DoesNotExist:
            logger.warning(f"Order {order_id} not found for payment intent")
    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")
        try:
            order = Order.objects.get(id=order_id)
            order.status = Order.STATUS_CANCELLED
            order.save()
        except Order.DoesNotExist:
            logger.warning(f"Order {order_id} not found for failed payment")

    return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)

