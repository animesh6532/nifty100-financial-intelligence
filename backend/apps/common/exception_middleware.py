import logging
from django.http import JsonResponse

logger = logging.getLogger('django')

class CustomExceptionMiddleware:
    """
    Middleware to catch unhandled exceptions (500s) and format them as standard JSON API responses
    so the frontend never receives an HTML traceback.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(f"Unhandled Server Error: {exception}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': {
                'code': 500,
                'message': 'Internal Server Error. Please contact support.',
                'details': str(exception) # In prod, you might want to omit details or control via settings.DEBUG
            }
        }, status=500)
