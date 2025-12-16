from rest_framework import viewsets # type: ignore
from rest_framework.permissions import IsAdminUser # type: ignore
from products.models import ProductVariant,VariantValueAssignment
from products.serializers import ProductVariantSerializer,VariantValueAssignmentSerializer


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUser]


class VariantValueAssignmentViewSet(viewsets.ModelViewSet):
    queryset = VariantValueAssignment.objects.all()
    serializer_class = VariantValueAssignmentSerializer
    permission_classes = [IsAdminUser]

