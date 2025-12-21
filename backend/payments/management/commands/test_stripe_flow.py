import json
from django.core.management.base import BaseCommand # type: ignore
from django.test import Client # type: ignore
from django.urls import reverse # type: ignore
from orders.models import Order
from payments.gateway import StripeGateway
from django.conf import settings # type: ignore
from django.contrib.auth import get_user_model # type: ignore


settings.ALLOWED_HOSTS.append("testserver")


User = get_user_model()

class Command(BaseCommand):
    help = "Run full local Stripe payment + webhook test flow"

    def handle(self, *args, **options):
        self.stdout.write("Starting Stripe test flow...")

         # 1. Create test user
        user = User.objects.create_user(
            email="test100@example.com",
            password="password123"
        )

        # 2. Create test order (VALID MODEL FIELDS)
        order = Order.objects.create(
            user=user,
            status=Order.STATUS_PENDING,
            total_price=25.00,
        )

        self.stdout.write(f"Created order #{order.id}")

        # 3. Create PaymentIntent
        intent = StripeGateway.create_payment_intent(
            amount=2500,  # cents
            currency="eur",
            metadata={"order_id": str(order.id)},
        )

        self.stdout.write(f"Created PaymentIntent {intent.id}")

        # 4. Simulate webhook payload
        payload = {
            "id": "evt_test_123",
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": intent.id,
                    "metadata": {
                        "order_id": str(order.id)
                    }
                }
            }
        }

        client = Client()

        response = client.post(
            reverse("stripe-webhook"),
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test",
        )

        order.refresh_from_db()

        # 5. Assertions
        assert response.status_code == 200
        assert order.status == Order.STATUS_PAID
        assert order.payment_intent_id == intent.id

        self.stdout.write(self.style.SUCCESS("Stripe test flow PASSED"))
