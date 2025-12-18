from rest_framework import viewsets, mixins, status# type: ignore
from .models import CartItem,get_or_create_cart
from .serializers import CartSerializer,CartItemSerializer,CartItemWriteSerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.response import Response # type: ignore



class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    

class CartItemViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CartItemWriteSerializer
        return CartItemSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        status_code = (
            status.HTTP_201_CREATED
            if serializer.created
            else status.HTTP_200_OK
        )

        return Response(
            CartItemSerializer(item).data,
            status=status_code,
        )


    
    def partial_update(self, request, *args, **kwargs):
        item = self.get_object()
        quantity = request.data.get("quantity")

        if quantity == 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) # type: ignore

        serializer = self.get_serializer(
            item, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    

