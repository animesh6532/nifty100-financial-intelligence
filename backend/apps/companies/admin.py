from django.contrib import admin
from .models import Company, FinancialData


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'sector', 'market_cap']
    list_filter = ['sector', 'created_at']
    search_fields = ['name', 'symbol', 'industry']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FinancialData)
class FinancialDataAdmin(admin.ModelAdmin):
    list_display = ['company', 'fiscal_year', 'quarter', 'revenue', 'net_income']
    list_filter = ['fiscal_year', 'quarter', 'company']
    search_fields = ['company__name', 'company__symbol']
    readonly_fields = ['created_at', 'updated_at']
