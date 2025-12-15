from rest_framework import serializers # type: ignore
from .models import Product,ProductVariant,VariantAttributeValue
from categories.models import Category
from categories.serializers import CategorySerializer


class ProductVariantSerializer(serializers.ModelSerializer):
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


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
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
            "is_active",
            "variants",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")
        return value
    


class VariantAttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()

    class Meta:
        model = VariantAttributeValue
        fields = ["attribute", "value"]
    

