from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, ScreenerAPIView

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
    path('screener/', ScreenerAPIView.as_view(), name='screener'),
]
