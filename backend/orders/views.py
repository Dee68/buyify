from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError # type: ignore
from rest_framework import permissions,status,viewsets # type: ignore
from products.models import ProductVariant
from cart.models import get_or_create_cart,Cart
from rest_framework.response import Response # type: ignore
from .serializers import OrderSerializer
from .models import Order,OrderItem


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
        cart_items = (
            cart.items
            .select_related("variant")
        )

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Lock all variants involved in checkout
        variant_ids = cart_items.values_list("variant_id", flat=True)

        variants = (
            ProductVariant.objects
            .select_for_update()
            .filter(id__in=variant_ids, is_active=True)
        )

        variant_map = {v.id: v for v in variants}

        # 2. Validate stock under lock
        for item in cart_items:
            variant = variant_map.get(item.variant_id)

            if not variant:
                raise ValidationError("Variant unavailable.")

            if item.quantity > variant.stock:
                raise ValidationError(
                    f"Insufficient stock for {variant.sku}."
                )

        # 3. Create order with frozen price
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
        )

        # 4. Create order items and deduct stock
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

        # 5. Clear cart
        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

