from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError # type: ignore
from rest_framework import permissions,status,viewsets # type: ignore
from products.models import ProductVariant
from cart.models import get_or_create_cart,Cart
from rest_framework.response import Response # type: ignore
from .serializers import OrderSerializer
from .models import Order,OrderItem
from rest_framework.decorators import action # type: ignore
from payments.gateway import StripeGateway


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart = get_or_create_cart(request.user)
        cart_items = cart.items.select_related("variant")

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Lock variants
        variant_ids = cart_items.values_list("variant_id", flat=True)
        variants = ProductVariant.objects.select_for_update().filter(
            id__in=variant_ids, is_active=True
        )
        variant_map = {v.id: v for v in variants}

        # Validate stock
        for item in cart_items:
            variant = variant_map.get(item.variant_id)
            if not variant:
                raise ValidationError("Variant unavailable.")
            if item.quantity > variant.stock:
                raise ValidationError(f"Insufficient stock for {variant.sku}.")

        # Create order with frozen price
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
        )

        # Create order items and deduct stock
        for item in cart_items:
            variant = variant_map[item.variant_id]
            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=item.quantity,
                unit_price=variant.price,
            )
            variant.stock = F("stock") - item.quantity
            variant.save(update_fields=["stock"])

        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def create_payment_intent(self, request, pk=None):
        order = self.get_object()

        if order.status != Order.STATUS_PENDING:
            return Response(
                {"detail": "Order not payable"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Amount in cents
        #amount_cents = int(order.total_price * 100)
        gateway = StripeGateway()

        # Create or retrieve PaymentIntent
        if order.payment_intent_id:
            intent = gateway.retrieve_payment_intent(order.payment_intent_id)
        else:
            intent = gateway.create_payment_intent(
                amount=order.total_price,
                #currency="usd",
                metadata={"order_id": order.id},
            )
            order.payment_intent_id = intent.id
            order.save(update_fields=["payment_intent_id"])

        return Response({"client_secret": intent.client_secret})