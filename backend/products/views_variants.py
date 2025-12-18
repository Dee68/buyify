from rest_framework import viewsets # type: ignore
from rest_framework.permissions import IsAdminUser # type: ignore
from products.models import ProductVariant,VariantValueAssignment
from products.serializers import ProductVariantSerializer,VariantValueAssignmentSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse # type: ignore


@extend_schema(
    description="""
    Products endpoint.

    Pricing & stock rules:
    - If product has active variants:
        - price = lowest variant price
        - stock = sum of active variant stock
    - Otherwise:
        - price and stock come from product fields
    """
)
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Create product variant (admin only)",
        description="""
        Create a product variant.

        Permissions:
        - Admin users only

        Business rules:
        - SKU must be unique
        - Only active variants affect product price and stock
        """,
        responses={
            201: ProductVariantSerializer,
            403: OpenApiResponse(description="Admin access required"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class VariantValueAssignmentViewSet(viewsets.ModelViewSet):
    queryset = VariantValueAssignment.objects.all()
    serializer_class = VariantValueAssignmentSerializer
    permission_classes = [IsAdminUser]

