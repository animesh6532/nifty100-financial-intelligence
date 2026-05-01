from rest_framework import serializers
from backend.apps.companies.models import Company, Sector, ProfitLoss, BalanceSheet, MLScore, HealthLabel

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['sector_id', 'sector_name']

class HealthLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthLabel
        fields = ['label_name', 'description']

class MLScoreSerializer(serializers.ModelSerializer):
    label = HealthLabelSerializer(read_only=True)
    
    class Meta:
        model = MLScore
        fields = [
            'health_score', 'label', 'anomaly_flag', 'anomaly_score', 
            'forecasted_revenue_1yr', 'forecasted_revenue_3yr'
        ]

class ProfitLossSerializer(serializers.ModelSerializer):
    year_value = serializers.IntegerField(source='year.year_value', read_only=True)
    
    class Meta:
        model = ProfitLoss
        exclude = ['company', 'year', 'created_at']

class BalanceSheetSerializer(serializers.ModelSerializer):
    year_value = serializers.IntegerField(source='year.year_value', read_only=True)
    
    class Meta:
        model = BalanceSheet
        exclude = ['company', 'year']

class CompanyListSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.sector_name', read_only=True)
    health_score = serializers.DecimalField(source='ml_score.health_score', max_digits=5, decimal_places=2, read_only=True)
    health_label = serializers.CharField(source='ml_score.label.label_name', read_only=True)
    
    class Meta:
        model = Company
        fields = [
            'company_id', 'symbol', 'company_name', 'sector_name', 'industry', 
            'market_cap_cr', 'current_price', 'pe_ratio', 'health_score', 'health_label'
        ]

class CompanyDetailSerializer(serializers.ModelSerializer):
    sector = SectorSerializer(read_only=True)
    ml_score = MLScoreSerializer(read_only=True)
    profit_loss = ProfitLossSerializer(many=True, read_only=True)
    balance_sheet = BalanceSheetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Company
        fields = '__all__'
