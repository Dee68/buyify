from rest_framework import viewsets, permissions, filters # type: ignore
from .models import Product
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from .filters import ProductFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter # type: ignore

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="category",
            description="Category slug (e.g. electronics)",
            required=False,
            type=str,
        )
    ]
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter, 
        filters.OrderingFilter,
        ]

    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']



