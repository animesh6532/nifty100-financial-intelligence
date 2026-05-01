import hmac
import hashlib
import time
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from backend.apps.api_keys.models import APIKey
from django.conf import settings

class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class validating API Keys.
    For POST requests with webhooks, we also enforce HMAC-SHA256 signature validation.
    """
    
    def authenticate(self, request):
        api_key_header = request.META.get('HTTP_X_API_KEY')
        
        if not api_key_header:
            return None # Move to next authentication class (e.g., JWT for frontend)

        try:
            api_key = APIKey.objects.get(key=api_key_header, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid or inactive API Key.')

        # If it's a POST request (e.g. creating webhooks), enforce HMAC signature for extra security
        if request.method in ['POST', 'PUT', 'PATCH']:
            signature = request.META.get('HTTP_X_SIGNATURE')
            timestamp = request.META.get('HTTP_X_TIMESTAMP')
            
            if not signature or not timestamp:
                raise AuthenticationFailed('Missing X-Signature or X-Timestamp headers for state-changing request.')
                
            # Prevent replay attacks (e.g. 5 minute window)
            try:
                ts = int(timestamp)
                if abs(time.time() - ts) > 300:
                    raise AuthenticationFailed('Request timestamp is too old (Replay attack prevention).')
            except ValueError:
                raise AuthenticationFailed('Invalid timestamp format.')

            # Verify HMAC
            # Note: In a real scenario, the secret is provided to the user once and stored hashed.
            # For this MVP, we assume `secret_hash` contains a simple secret or we use Django's secret key.
            # Using simple shared secret logic for demonstration:
            payload = f"{timestamp}.{request.body.decode('utf-8')}".encode('utf-8')
            expected_sig = hmac.new(
                settings.SECRET_KEY.encode('utf-8'), 
                payload, 
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_sig, signature):
                raise AuthenticationFailed('Invalid HMAC signature.')

        return (api_key.user, api_key)
