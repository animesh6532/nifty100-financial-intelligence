from rest_framework import routers
from .views import MLScoreViewSet, AnomalyViewSet, ClusterViewSet, ForecastViewSet

router = routers.DefaultRouter()
router.register(r'scores', MLScoreViewSet)
router.register(r'anomalies', AnomalyViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'forecasts', ForecastViewSet)

urlpatterns = router.urls
