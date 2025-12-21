import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeGateway:
    @staticmethod
    def create_payment_intent(amount: int, currency: str = "eur", metadata: dict | None = None):
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata=metadata or {},
        )

    @staticmethod
    def retrieve_payment_intent(payment_intent_id: str):
        return stripe.PaymentIntent.retrieve(payment_intent_id)

    @staticmethod
    def confirm_payment_intent(payment_intent_id: str):
        return stripe.PaymentIntent.confirm(payment_intent_id)
    
    @staticmethod
    def create_refund(payment_intent_id: str, amount: int | None = None):
        """
        Create a refund.
        Amount is optional (partial refunds supported).
        """
        return stripe.Refund.create(
            payment_intent=payment_intent_id,
            amount=amount,
        )
