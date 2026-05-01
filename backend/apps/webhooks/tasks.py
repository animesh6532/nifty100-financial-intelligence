import json
import hmac
import hashlib
import time
import requests
import logging
from celery import shared_task
from django.conf import settings
from backend.apps.webhooks.models import WebhookSubscription, WebhookDeliveryLog
from backend.apps.api_keys.models import APIKey

logger = logging.getLogger(__name__)

def generate_webhook_signature(payload: str, secret: str, timestamp: str) -> str:
    """Generates HMAC-SHA256 signature for the webhook payload."""
    sig_payload = f"{timestamp}.{payload}".encode('utf-8')
    return hmac.new(secret.encode('utf-8'), sig_payload, hashlib.sha256).hexdigest()

@shared_task(bind=True, max_retries=5)
def send_webhook(self, subscription_id: str, payload_data: dict):
    """
    Sends a webhook payload to the subscribed URL.
    Implements exponential backoff on failure.
    """
    try:
        subscription = WebhookSubscription.objects.get(id=subscription_id, is_active=True)
    except WebhookSubscription.DoesNotExist:
        logger.warning(f"Webhook subscription {subscription_id} not found or inactive.")
        return

    payload_str = json.dumps(payload_data)
    timestamp = str(int(time.time()))
    
    # In a real system, the subscription would have its own secret, 
    # or it would be tied to the API Key of the user. We assume the latter here.
    try:
        api_key_obj = APIKey.objects.get(user=subscription.user, is_active=True)
        secret = api_key_obj.secret_hash # For demonstration, assuming this contains the secret
    except APIKey.DoesNotExist:
        secret = settings.SECRET_KEY # Fallback
        
    signature = generate_webhook_signature(payload_str, secret, timestamp)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Webhook-Signature': signature,
        'X-Webhook-Timestamp': timestamp,
        'X-Webhook-Event': subscription.event_type
    }
    
    # Create log entry
    log = WebhookDeliveryLog.objects.create(
        subscription=subscription,
        payload=payload_data,
        attempt_count=self.request.retries + 1
    )
    
    try:
        response = requests.post(subscription.target_url, data=payload_str, headers=headers, timeout=10)
        
        log.response_status = response.status_code
        log.response_body = response.text[:1000] # Truncate large responses
        
        if 200 <= response.status_code < 300:
            log.success = True
            log.save()
            logger.info(f"Successfully delivered webhook {subscription.id} to {subscription.target_url}")
        else:
            log.success = False
            log.save()
            logger.warning(f"Webhook {subscription.id} failed with status {response.status_code}")
            
            # Retry with exponential backoff: 2^retry_count * 10 seconds (e.g. 10s, 20s, 40s, 80s)
            countdown = (2 ** self.request.retries) * 10
            raise self.retry(countdown=countdown)
            
    except requests.exceptions.RequestException as e:
        log.success = False
        log.response_body = str(e)
        log.save()
        logger.error(f"Network error delivering webhook {subscription.id}: {e}")
        countdown = (2 ** self.request.retries) * 10
        raise self.retry(exc=e, countdown=countdown)
