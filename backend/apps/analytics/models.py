from django.db import models


class FinancialMetrics(models.Model):
    company = models.OneToOneField('companies.Company', on_delete=models.CASCADE)
    
    # Liquidity Ratios
    current_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    quick_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Profitability Ratios
    gross_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    operating_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    net_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    roe = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    roa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Valuation Ratios
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pb_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Debt Ratios
    debt_to_equity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'financial_metrics'
    
    def __str__(self):
        return f"{self.company.name} Metrics"
