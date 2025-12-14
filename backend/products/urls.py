from rest_framework import routers # type: ignore
from .views import ProductViewSet

app_name = "products"

router = routers.DefaultRouter()
router.register("", ProductViewSet, basename="products")

urlpatterns = router.urls
