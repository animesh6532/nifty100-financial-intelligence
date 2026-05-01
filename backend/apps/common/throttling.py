from rest_framework.throttling import SimpleRateThrottle
from backend.apps.api_keys.models import APIKey

class TieredRateThrottle(SimpleRateThrottle):
    """
    Custom throttle class that applies limits based on the API Key's tier.
    BASIC: 10/min, 100/hour
    PRO: 60/min, 1000/hour
    ENTERPRISE: 300/min, 10000/hour
    """
    scope = 'tiered'

    def get_cache_key(self, request, view):
        if not request.auth or not isinstance(request.auth, APIKey):
            # If not authenticated via API Key, apply default anonymous limit
            return self.cache_format % {
                'scope': 'anon',
                'ident': self.get_ident(request)
            }
        
        # Cache key based on the API Key token
        return self.cache_format % {
            'scope': request.auth.tier,
            'ident': request.auth.key
        }

    def get_rate(self):
        # We override allow_request to handle dynamic rates better, 
        # but DRF requires get_rate to return a string for initialization if not dynamic.
        # We'll use dynamic parsing below.
        pass

    def allow_request(self, request, view):
        if not request.auth or not isinstance(request.auth, APIKey):
            self.rate = '10/m' # Default anon rate
            self.num_requests, self.duration = self.parse_rate(self.rate)
            return super().allow_request(request, view)

        tier = request.auth.tier
        
        # Set rate based on tier
        if tier == 'BASIC':
            self.rate = '10/m'
        elif tier == 'PRO':
            self.rate = '60/m'
        elif tier == 'ENTERPRISE':
            self.rate = '300/m'
        else:
            self.rate = '10/m'

        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)
