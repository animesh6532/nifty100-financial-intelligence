import django_filters
from .models import Company


class CompanyFilter(django_filters.FilterSet):
    sector = django_filters.CharFilter(field_name='sector', lookup_expr='icontains')
    market_cap_min = django_filters.NumberFilter(field_name='market_cap', lookup_expr='gte')
    market_cap_max = django_filters.NumberFilter(field_name='market_cap', lookup_expr='lte')
    
    class Meta:
        model = Company
        fields = ['sector', 'market_cap_min', 'market_cap_max']
