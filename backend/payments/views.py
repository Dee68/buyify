from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status # type: ignore
from django.conf import settings
from orders.models import Order
from .gateway import stripe
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    #endpoint_secret = getattr(stripe, "WEBHOOK_SECRET", None)
    event=None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)

    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")
        try:
            order = Order.objects.get(id=order_id)
            order.payment_intent_id = intent["id"]
            order.status = Order.STATUS_PAID
            order.save()
        except Order.DoesNotExist:
            pass  # optionally log the missing order

    return JsonResponse({"status": "success"}, status=200)

