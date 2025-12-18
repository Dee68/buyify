from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status,permissions # type: ignore
from .models import CartItem,get_or_create_cart
from .serializers import CartItemSerializer,CartItemWriteSerializer

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartItemWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        variant = serializer.validated_data["variant"]
        quantity = serializer.validated_data["quantity"]

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={"quantity": quantity},
        )

        if not created:
            item.quantity += quantity
            item.save()
            return Response(
                CartItemSerializer(item).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            CartItemSerializer(item).data,
            status=status.HTTP_201_CREATED,
        )
