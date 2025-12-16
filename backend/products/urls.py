from rest_framework import routers # type: ignore
from .views import ProductViewSet
from .views_variants import ProductVariantViewSet

app_name = "products"

router = routers.DefaultRouter()
router.register("", ProductViewSet, basename="products")
router.register(
    r"variants",
    ProductVariantViewSet,
    basename="variants"
)


urlpatterns = router.urls
