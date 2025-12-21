from django.conf import settings # type: ignore
from django.db import models # type: ignore
from products.models import ProductVariant
from django.utils import timezone # type: ignore
from django.core.exceptions import ValidationError # type: ignore


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"
    STATUS_REFUNDED = "refunded"
    STATUS_DISPUTED = "disputed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_REFUNDED, "Refunded"),
        (STATUS_DISPUTED, "Disputed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )
    refund_id = models.CharField(max_length=255, blank=True, null=True)
    dispute_id = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def mark_paid(self, payment_intent_id: str):
        if self.status != self.STATUS_PENDING:
            raise ValidationError("Order cannot be paid")

        self.status = self.STATUS_PAID
        self.payment_intent_id = payment_intent_id
        self.paid_at = timezone.now()
        self.save(update_fields=[
            "status",
            "payment_intent_id",
            "paid_at",
        ])

    def cancel(self):
        if self.status != self.STATUS_PENDING:
            raise ValidationError("Only pending orders can be cancelled")

        self.status = self.STATUS_CANCELLED
        self.save(update_fields=["status"])

    def __str__(self):
        return f"Order #{self.id} ({self.user})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def line_total(self):
        return self.unit_price * self.quantity
