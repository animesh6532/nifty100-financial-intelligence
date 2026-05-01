from django.db import models


class MLScore(models.Model):
    company = models.OneToOneField('companies.Company', on_delete=models.CASCADE)
    health_score = models.DecimalField(max_digits=5, decimal_places=2)
    growth_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    debt_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    efficiency_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company.name} - Health Score: {self.health_score}"


class Anomaly(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100)
    expected_value = models.DecimalField(max_digits=15, decimal_places=2)
    actual_value = models.DecimalField(max_digits=15, decimal_places=2)
    deviation_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    severity = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ])
    detected_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.metric_name}"


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    companies = models.ManyToManyField('companies.Company')
    characteristics = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Forecast(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    metric = models.CharField(max_length=100)
    forecast_date = models.DateField()
    predicted_value = models.DecimalField(max_digits=15, decimal_places=2)
    confidence_interval = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-forecast_date']
    
    def __str__(self):
        return f"{self.company.name} - {self.metric} Forecast"
