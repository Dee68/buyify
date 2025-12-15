from rest_framework import serializers # type: ignore
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "created_at")
        read_only_fields = ("id", "slug", "created_at")