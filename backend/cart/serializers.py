from rest_framework import serializers # type: ignore
from .models import Cart, CartItem, get_or_create_cart
from products.serializers import ProductVariantSerializer
from products.models import ProductVariant


class CartItemSerializer(serializers.ModelSerializer):
    variant = serializers.IntegerField(source="variant.id", read_only=True)
    

    class Meta:
        model = CartItem
        fields = ("id", "variant", "quantity")

    
    
class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("variant", "quantity")

    def validate(self, attrs):
        variant = attrs.get("variant") or self.instance.variant
        quantity = attrs.get("quantity")

        if not variant.is_active:
            raise serializers.ValidationError("Variant is inactive.")

        if quantity > variant.stock:
            raise serializers.ValidationError(
                "Quantity exceeds available stock."
            )
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        cart = get_or_create_cart(request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=validated_data["variant"],
            defaults={"quantity": validated_data["quantity"]},
        )

        if not created:
            item.quantity += validated_data["quantity"]
            item.save()

        self.created = created  # store flag
        return item






class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items","total_price", "total_items"]
