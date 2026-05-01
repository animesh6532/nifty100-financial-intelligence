from rest_framework import routers
from .views import APIKeyViewSet

router = routers.DefaultRouter()
router.register(r'keys', APIKeyViewSet)

urlpatterns = router.urls
