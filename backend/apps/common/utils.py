from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Standardize all DRF errors into a consistent response format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': str(exc),
                'details': response.data
            }
        }
        response.data = custom_response_data
    else:
        # Handle non-DRF exceptions (500s) if needed, 
        # though usually handled by middleware in prod.
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        
    return response

def api_success_response(data, message="Success", status_code=200, meta=None):
    """
    Standardized success response format.
    """
    response_data = {
        'success': True,
        'message': message,
        'data': data
    }
    if meta:
        response_data['meta'] = meta
        
    return Response(response_data, status=status_code)
