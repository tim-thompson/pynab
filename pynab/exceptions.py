class PynabException(Exception):
    """Base exception class for Pynab"""

    pass


class PynabAuthenticationException(PynabException):
    """Exception raised for authentication errors in a request"""

    pass


class PynabResourceDoesNotExist(PynabException):
    """Exception raised when a requested resource is not found"""

    pass


class PynabRateLimitExceededException(PynabException):
    """Exception raised when a rate limit exceed response is received"""

    pass
