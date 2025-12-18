from django.conf import settings # type: ignore
from django.db import models # type: ignore
from products.models import ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="cart",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(
            item.variant.price * item.quantity
            for item in self.items.select_related("variant")
            if item.variant.is_active
        )

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    

    def __str__(self):
        return f"Cart ({self.user})"
    
# ===============
# Helper function
# ================
def get_or_create_cart(user):
    return Cart.objects.get_or_create(user=user)[0]



class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE,
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "variant")

    def __str__(self):
        return f"{self.variant.sku} x {self.quantity}"

