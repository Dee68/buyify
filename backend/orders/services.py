from django.db import transaction # type: ignore
from cart.models import Cart
from .models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(cart: Cart):
    if not cart.items.exists():
        raise ValueError("Cart is empty")

    order = Order.objects.create(
        user=cart.user,
        total_price=cart.total_price,
    )

    items = []
    for item in cart.items.select_related("variant"):
        items.append(
            OrderItem(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                unit_price=item.variant.price,
            )
        )

    OrderItem.objects.bulk_create(items)

    cart.items.all().delete()

    return order
