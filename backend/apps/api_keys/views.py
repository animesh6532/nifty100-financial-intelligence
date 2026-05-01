from rest_framework import viewsets
from .models import APIKey


class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    # Add serializer
