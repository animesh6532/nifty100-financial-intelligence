from rest_framework import routers
from .views import PartnerCompanyViewSet

router = routers.DefaultRouter()
router.register(r'companies', PartnerCompanyViewSet)

urlpatterns = router.urls
