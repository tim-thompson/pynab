class PynabError(Exception):
    """Base exception class for Pynab"""

    pass


class PynabBadRequestError(PynabError):
    """Exception raised when API reports a bad request"""

    pass


class PynabAuthenticationError(PynabError):
    """Exception raised for authentication errors in a request"""

    pass


class PynabResourceDoesNotExist(PynabError):
    """Exception raised when a requested resource is not found"""

    pass


class PynabRateLimitExceededError(PynabError):
    """Exception raised when a rate limit exceed response is received"""

    pass
