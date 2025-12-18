from rest_framework import serializers # type: ignore
from .models import Product,ProductVariant,VariantAttributeValue,VariantValueAssignment
from categories.models import Category
from categories.serializers import CategorySerializer
from decimal import Decimal
from drf_spectacular.utils import extend_schema_field # type: ignore


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Product variant.

    Notes:
    - Only active variants affect product price and stock
    - Inactive variants are ignored in calculations
    - Admin-only write access
    """
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "price",
            "stock",
            "is_active",
            "attributes",
        ]

    def get_attributes(self, obj):
        values = obj.attribute_values.select_related(
            "attribute_value__attribute"
        )
        return [
            {
                "name": v.attribute_value.attribute.name,
                "value": v.attribute_value.value,
            }
            for v in values
        ]

class ProductWriteSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0
    )
    stock = serializers.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "is_active",
        )


class ProductSerializer(serializers.ModelSerializer):
    resolved_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    resolved_stock = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    variants = ProductVariantSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    price = serializers.DecimalField(
        source="resolved_price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
        min_value=0,
        help_text="Resolved price from active variants or base product price",
    )
    stock = serializers.IntegerField(
        source="aggregated_stock",
        read_only=True,
        help_text="Aggregated stock from active variants only",
    )


    category_detail = CategorySerializer(source="category", read_only=True)
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "category",
            "category_detail",
            "created_at",
            "updated_at",
            "resolved_price",
            "resolved_stock",
            "is_available",
            "is_active",
            "variants",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")


    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")
        return value
    


class VariantAttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()

    class Meta:
        model = VariantAttributeValue
        fields = ["attribute", "value"]

class VariantValueAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantValueAssignment
        fields = ["id", "variant", "attribute_value"]

    

