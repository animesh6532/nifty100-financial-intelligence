from rest_framework import routers
from .views import FinancialMetricsViewSet

router = routers.DefaultRouter()
router.register(r'metrics', FinancialMetricsViewSet)

urlpatterns = router.urls
