from rest_framework import viewsets
from .models import Screen


class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    # Add serializer
