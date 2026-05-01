from django.db import models
from django.contrib.auth.models import User
import uuid

class WebhookSubscription(models.Model):
    EVENT_CHOICES = (
        ('score_updated', 'ML Score Updated'),
        ('anomaly_detected', 'Anomaly Detected'),
        ('forecast_generated', 'Forecast Generated'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webhooks')
    target_url = models.URLField(max_length=500)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event_type} -> {self.target_url}"


class WebhookDeliveryLog(models.Model):
    subscription = models.ForeignKey(WebhookSubscription, on_delete=models.CASCADE, related_name='logs')
    payload = models.JSONField()
    response_status = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)
    success = models.BooleanField(default=False)
    attempt_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.subscription.id} - Success: {self.success}"
