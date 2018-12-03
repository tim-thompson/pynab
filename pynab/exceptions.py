class PynabError(Exception):
    """Base exception class for Pynab"""

    pass


class PynabBadRequestError(PynabError):
    """Exception raised when API reports a bad request"""

    pass


class PynabAuthenticationError(PynabError):
    """Exception raised for authentication errors in a request"""

    pass


class PynabAccountError(PynabError):
    """Exception raised when there is an error accessing the API due to a subscription or trial expiration"""

    pass


class PynabNotFoundError(PynabError):
    """Exception raised when a requested resource is not found"""

    pass


class PynabConflictError(PynabError):
    """
    Exception raised when a resource cannot be saved during a
    POST or PUT due to a conflict with an existing resource
    """

    pass


class PynabRateLimitExceededError(PynabError):
    """Exception raised when a rate limit exceed response is received"""

    pass


class PynabInternalServerError(PynabError):
    """Exception raised when an internal server error is returned from the YNAB API"""

    pass


class PynabConnectionError(PynabError):
    """Exception raised when a connection fails to be made to the YNAB API"""

    pass
