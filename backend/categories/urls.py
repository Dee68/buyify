from rest_framework.routers import DefaultRouter # type: ignore
from .views import CategoryViewSet

app_name="categories"

router = DefaultRouter()
router.register("", CategoryViewSet, basename="categories")

urlpatterns = router.urls
