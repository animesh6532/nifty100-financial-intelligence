from django.db import models

class Sector(models.Model):
    sector_id = models.AutoField(primary_key=True)
    sector_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dim_sector'
        managed = False  # Managed by ETL/SQL directly

    def __str__(self):
        return self.sector_name


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=255)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, db_column='sector_id')
    industry = models.CharField(max_length=100, null=True, blank=True)
    market_cap_cr = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    current_price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    roce = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    roe = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dim_company'
        managed = False

    def __str__(self):
        return self.symbol


class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year_value = models.IntegerField(unique=True)
    financial_year = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'dim_year'
        managed = False

    def __str__(self):
        return str(self.financial_year)


class HealthLabel(models.Model):
    label_id = models.AutoField(primary_key=True)
    label_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'dim_health_label'
        managed = False

    def __str__(self):
        return self.label_name


class ProfitLoss(models.Model):
    pl_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id', related_name='profit_loss')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, db_column='year_id')
    revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    operating_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opm_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    eps = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fact_profit_loss'
        managed = False
        unique_together = (('company', 'year'),)


class BalanceSheet(models.Model):
    bs_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id', related_name='balance_sheet')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, db_column='year_id')
    equity_capital = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    borrowings = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        db_table = 'fact_balance_sheet'
        managed = False


class MLScore(models.Model):
    score_id = models.AutoField(primary_key=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, db_column='company_id', related_name='ml_score')
    health_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    label = models.ForeignKey(HealthLabel, on_delete=models.SET_NULL, null=True, db_column='label_id')
    anomaly_flag = models.BooleanField(default=False)
    anomaly_score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    forecasted_revenue_1yr = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    forecasted_revenue_3yr = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        db_table = 'fact_ml_scores'
        managed = False
