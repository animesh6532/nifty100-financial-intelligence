from rest_framework import serializers


class PartnerCompanySerializer(serializers.Serializer):
    name = serializers.CharField()
    symbol = serializers.CharField()
    sector = serializers.CharField()
    market_cap = serializers.IntegerField()
