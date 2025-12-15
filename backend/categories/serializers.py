from rest_framework import serializers # type: ignore
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ["id", "name", "slug","parent","product_count","children"]
        read_only_fields = ("id", "slug", "created_at")

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data