from rest_framework import serializers # type: ignore
from .models import Order, OrderItem
#from decimal import Decimal




class OrderItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.SerializerMethodField()

    def get_unit_price(self, obj):
        return format(obj.unit_price, "f").rstrip("0").rstrip(".")
    class Meta:
        model = OrderItem
        fields = ("variant", "quantity", "unit_price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return format(obj.total_price, "f").rstrip("0").rstrip(".")

    class Meta:
        model = Order
        fields = (
            "id",
            "total_price",
            "created_at",
            "items",
        )
