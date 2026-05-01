from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None
        
        # Validate API key
        try:
            from apps.api_keys.models import APIKey
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            return (api_key_obj.user, None)
        except:
            raise AuthenticationFailed('Invalid API key')
