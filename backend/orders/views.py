from rest_framework import viewsets, permissions, status # type: ignore
from rest_framework.response import Response # type: ignore
from django.db import transaction # type: ignore

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem


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
        cart_items = CartItem.objects.select_related(
            "variant", "variant__product"
        ).filter(cart__user=request.user)

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        

        total_price = 0

        for item in cart_items:
            unit_price = item.variant.price
            total_price += unit_price * item.quantity

        order = Order.objects.create(user=request.user,total_price=total_price,)

        OrderItem.objects.create(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                unit_price=unit_price,
            )

        order.total_price = total_price
        order.save()

        # Clear cart
        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
