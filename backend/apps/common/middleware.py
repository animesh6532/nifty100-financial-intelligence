from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class CustomExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(f"Exception: {str(exception)}")
        return None
