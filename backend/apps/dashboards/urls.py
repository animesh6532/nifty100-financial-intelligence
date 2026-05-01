from rest_framework import routers
from .views import DashboardViewSet

router = routers.DefaultRouter()
router.register(r'dashboards', DashboardViewSet, basename='dashboard')

urlpatterns = router.urls
