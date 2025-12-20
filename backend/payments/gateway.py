import stripe # type: ignore
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeGateway:
    @staticmethod
    def create_payment_intent(amount: int, currency: str = "usd", metadata: dict = None):
        """
        Create a Stripe PaymentIntent.
        Amount is in cents.
        """
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata=metadata or {},
        )
        return intent

    @staticmethod
    def retrieve_payment_intent(payment_intent_id: str):
        """
        Retrieve a Stripe PaymentIntent by ID.
        """
        return stripe.PaymentIntent.retrieve(payment_intent_id)

    @staticmethod
    def confirm_payment_intent(payment_intent_id: str):
        """
        Confirm a PaymentIntent manually if needed.
        """
        return stripe.PaymentIntent.confirm(payment_intent_id)
