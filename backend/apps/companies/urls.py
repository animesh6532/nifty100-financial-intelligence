from rest_framework import routers
from .views import CompanyViewSet, FinancialDataViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'financial-data', FinancialDataViewSet)

urlpatterns = router.urls
