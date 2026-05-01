import time
import logging
import json

logger = logging.getLogger('api_request_logger')

class APILoggingMiddleware:
    """
    Middleware to log all incoming API requests and their processing times.
    Useful for analytics and debugging.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        # Only log API requests
        if request.path.startswith('/api/'):
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'ip': self._get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')
            }
            
            if response.status_code >= 400:
                logger.error(f"API Error: {json.dumps(log_data)}")
            else:
                logger.info(f"API Request: {json.dumps(log_data)}")
                
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
