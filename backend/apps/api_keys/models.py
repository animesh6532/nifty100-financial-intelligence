from django.db import models
import uuid


class APIKey(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='api_key')
    key = models.CharField(max_length=40, unique=True, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} API Key"
