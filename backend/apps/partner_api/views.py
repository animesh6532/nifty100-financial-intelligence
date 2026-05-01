from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.companies.models import Company
from .serializers import PartnerCompanySerializer
from .authentication import APIKeyAuthentication


class PartnerCompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = PartnerCompanySerializer
    authentication_classes = [APIKeyAuthentication]


@api_view(['GET'])
def partner_status(request):
    return Response({'status': 'active'})
