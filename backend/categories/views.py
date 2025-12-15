from rest_framework import viewsets, permissions # type: ignore
from .models import Category
from .serializers import CategorySerializer,CategoryTreeSerializer
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request):
        queryset = (
            self.get_queryset()
            .filter(parent__isnull=True)
            .prefetch_related("children__children")
        )

        serializer = CategoryTreeSerializer(queryset, many=True)
        return Response(serializer.data)
