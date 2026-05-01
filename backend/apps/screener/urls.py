from rest_framework import routers
from .views import ScreenViewSet

router = routers.DefaultRouter()
router.register(r'screens', ScreenViewSet)

urlpatterns = router.urls
