from rest_framework.routers import DefaultRouter # type: ignore
from django.urls import path# type: ignore
from .views import CartView,CartItemViewSet

app_name="cart"

cart_router = DefaultRouter()
cart_router.register(r"items", CartItemViewSet, basename="cart-items")



urlpatterns = [
    path("", CartView.as_view(), name="cart"),
]

urlpatterns += cart_router.urls
