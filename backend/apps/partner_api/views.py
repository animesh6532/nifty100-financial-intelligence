from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from backend.apps.companies.models import Company
from backend.apps.common.auth import APIKeyAuthentication
from backend.apps.common.throttling import TieredRateThrottle
from .serializers import CompanyListSerializer, CompanyDetailSerializer
import logging

logger = logging.getLogger(__name__)

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows companies to be viewed or searched.
    Rate limited by API Key tier. Cached by Redis.
    """
    queryset = Company.objects.select_related('sector', 'ml_score', 'ml_score__label').all()
    authentication_classes = [APIKeyAuthentication]
    throttle_classes = [TieredRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering & Search
    filterset_fields = ['sector__sector_name', 'industry', 'ml_score__label__label_name']
    search_fields = ['symbol', 'company_name']
    ordering_fields = ['market_cap_cr', 'pe_ratio', 'current_price', 'ml_score__health_score']
    ordering = ['-market_cap_cr']  # Default ordering

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanyListSerializer
        return CompanyDetailSerializer

    # Cache list endpoint for 5 minutes (300 seconds)
    @method_decorator(cache_page(300, key_prefix='company_list'))
    def list(self, request, *args, **kwargs):
        logger.info(f"Company list requested by user: {request.user}")
        return super().list(request, *args, **kwargs)

    # Cache detail endpoint for 15 minutes
    @method_decorator(cache_page(900, key_prefix='company_detail'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ScreenerAPIView(generics.ListAPIView):
    """
    Advanced screener endpoint to filter companies by complex criteria.
    e.g., ?min_pe=10&max_pe=30&min_health=80
    """
    serializer_class = CompanyListSerializer
    authentication_classes = [APIKeyAuthentication]
    throttle_classes = [TieredRateThrottle]

    def get_queryset(self):
        queryset = Company.objects.select_related('sector', 'ml_score', 'ml_score__label').all()
        
        # Custom filtering logic
        min_pe = self.request.query_params.get('min_pe')
        max_pe = self.request.query_params.get('max_pe')
        min_health = self.request.query_params.get('min_health')
        
        if min_pe: queryset = queryset.filter(pe_ratio__gte=min_pe)
        if max_pe: queryset = queryset.filter(pe_ratio__lte=max_pe)
        if min_health: queryset = queryset.filter(ml_score__health_score__gte=min_health)
        
        return queryset
