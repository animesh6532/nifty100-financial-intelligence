from rest_framework import serializers
from .models import Company, FinancialData


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'symbol', 'isin', 'sector', 'industry',
            'description', 'website', 'market_cap', 'employees',
            'founded_year', 'headquarters', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class FinancialDataSerializer(serializers.ModelSerializer):
    company_symbol = serializers.CharField(source='company.symbol', read_only=True)
    
    class Meta:
        model = FinancialData
        fields = [
            'id', 'company', 'company_symbol', 'quarter', 'fiscal_year',
            'revenue', 'operating_income', 'net_income', 'eps',
            'total_assets', 'total_liabilities', 'equity',
            'operating_cash_flow', 'capex', 'free_cash_flow',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CompanyDetailSerializer(CompanySerializer):
    financial_data = FinancialDataSerializer(many=True, read_only=True)
    
    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + ['financial_data']
