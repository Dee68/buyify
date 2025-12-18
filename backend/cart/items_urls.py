from rest_framework.routers import DefaultRouter # type: ignore
from .views import CartItemViewSet

router = DefaultRouter()
router.register(r"items", CartItemViewSet, basename="items")

urlpatterns = router.urls
