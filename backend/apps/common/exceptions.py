"""
Custom exceptions
"""


class APIException(Exception):
    pass


class ValidationError(APIException):
    pass


class NotFoundError(APIException):
    pass
