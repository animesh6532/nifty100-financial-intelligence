from rest_framework import viewsets
from .models import FinancialMetrics


class FinancialMetricsViewSet(viewsets.ModelViewSet):
    queryset = FinancialMetrics.objects.all()
    # Add serializer
