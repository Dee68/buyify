from rest_framework.routers import DefaultRouter # type: ignore
from .views import OrderViewSet

router = DefaultRouter()
router.register(r"", OrderViewSet, basename="orders")

urlpatterns = router.urls
