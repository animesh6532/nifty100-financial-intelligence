from rest_framework import viewsets
from .models import MLScore, Anomaly, Cluster, Forecast


class MLScoreViewSet(viewsets.ModelViewSet):
    queryset = MLScore.objects.all()
    # Add serializer


class AnomalyViewSet(viewsets.ModelViewSet):
    queryset = Anomaly.objects.all()
    # Add serializer


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    # Add serializer


class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    # Add serializer
