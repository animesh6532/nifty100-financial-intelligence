from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, FinancialData
from .serializers import CompanySerializer, FinancialDataSerializer, CompanyDetailSerializer
from .filters import CompanyFilter


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ['name', 'symbol', 'industry', 'sector']
    ordering_fields = ['name', 'market_cap', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer


class FinancialDataViewSet(viewsets.ModelViewSet):
    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['company', 'quarter', 'fiscal_year']
    ordering_fields = ['fiscal_year', 'quarter']
    ordering = ['-fiscal_year', '-quarter']
