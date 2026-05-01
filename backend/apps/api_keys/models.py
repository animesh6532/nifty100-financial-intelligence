from django.db import models
from django.contrib.auth.models import User
import secrets
import string

def generate_api_key():
    alphabet = string.ascii_letters + string.digits
    return 'pk_' + ''.join(secrets.choice(alphabet) for i in range(32))

class APIKey(models.Model):
    TIER_CHOICES = (
        ('BASIC', 'Basic'),
        ('PRO', 'Pro'),
        ('ENTERPRISE', 'Enterprise'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=50, help_text="A descriptive name for the key")
    key = models.CharField(max_length=40, unique=True, default=generate_api_key, editable=False)
    secret_hash = models.CharField(max_length=128, help_text="Bcrypt hash of the webhook secret")
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='BASIC')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.tier})"
