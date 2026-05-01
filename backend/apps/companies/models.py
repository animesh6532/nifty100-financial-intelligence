from django.db import models


class Company(models.Model):
    SECTOR_CHOICES = [
        ('IT', 'Information Technology'),
        ('BANK', 'Banking'),
        ('AUTO', 'Automobile'),
        ('PHARMA', 'Pharma'),
        ('FMCG', 'FMCG'),
        ('ENERGY', 'Energy'),
        ('METAL', 'Metals'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=10, unique=True)
    isin = models.CharField(max_length=12, unique=True)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    industry = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    employees = models.IntegerField(null=True, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    headquarters = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'companies'
    
    def __str__(self):
        return self.name


class FinancialData(models.Model):
    QUARTER_CHOICES = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financial_data')
    quarter = models.CharField(max_length=2, choices=QUARTER_CHOICES)
    fiscal_year = models.IntegerField()
    
    # Income Statement
    revenue = models.BigIntegerField(null=True, blank=True)
    operating_income = models.BigIntegerField(null=True, blank=True)
    net_income = models.BigIntegerField(null=True, blank=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Balance Sheet
    total_assets = models.BigIntegerField(null=True, blank=True)
    total_liabilities = models.BigIntegerField(null=True, blank=True)
    equity = models.BigIntegerField(null=True, blank=True)
    
    # Cash Flow
    operating_cash_flow = models.BigIntegerField(null=True, blank=True)
    capex = models.BigIntegerField(null=True, blank=True)
    free_cash_flow = models.BigIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('company', 'quarter', 'fiscal_year')
        ordering = ['-fiscal_year', '-quarter']
    
    def __str__(self):
        return f"{self.company.symbol} {self.fiscal_year} {self.quarter}"
