import pynab.pynab as pynab
from pynab.models import User, BudgetSummary, Budget, BudgetSettings, Transaction

from pynab.exceptions import (
    PynabError,
    PynabAuthenticationError,
    PynabNotFoundError,
    PynabRateLimitExceededError,
    PynabBadRequestError,
    PynabAccountError,
    PynabConflictError,
    PynabInternalServerError,
)

parse_errors = {
    "bad_request": PynabBadRequestError(
        "YNAB returned a bad request. This is likely a Pynab bug, please report on GitHub"
    ),
    "not_authorized": PynabAuthenticationError("Authentication with access token failed"),
    "subscription_lapsed": PynabAccountError(
        "Subscription lapsed, API access requires an active subscription or trial"
    ),
    "trial_expired": PynabAccountError(
        "Trial expired, API access requires an active subscription or trial"
    ),
    "not_found": PynabNotFoundError(
        "URI not found. This is likely a Pynab bug, please report on GitHub"
    ),
    "resource_not_found": PynabNotFoundError("Requested resource not found"),
    "conflict": PynabConflictError(
        "Could not complete operation, conflict with existing resource"
    ),
    "too_many_requests": PynabRateLimitExceededError("Rate limit exceeded, too many requests"),
    "internal_server_error": PynabInternalServerError(
        "An internal server error occurred. This is a YNAB problem, try again later"
    ),
}


def parse(json):
    """
    Client component for factory that accepts json returned from
    the YNAB API and parses it to establish what is contained within
    the response and create an appropriate object to represent the data
    :param json: json in the form a dict to be parsed to an appropriate object
    :return: Object created by parsing the json
    """
    if "error" in json:
        _handle_error_response(json["error"])

    parser = _get_parser(json["data"])
    return parser(json)


def _get_parser(data_type):
    """
    Creator component for factory that determines the type of data being
    parsed and returns the correct function to use for parsing the data
    :param data_type:
    :return: the correct method for parsing the requested data type
    """
    if "user" in data_type:
        return _parse_user
    elif "budgets" in data_type:
        return _parse_budgets
    elif "budget" in data_type:
        return _parse_budget
    elif "settings" in data_type:
        return _parse_settings
    elif "transaction" in data_type:
        return _parse_transaction
    elif "transactions" in data_type:
        return _parse_transactions
    else:
        # TODO: Create proper exception
        raise PynabError("Unable to parse response from YNAB API")


def _parse_user(json):
    """
    Product component for factory that creates a User object from user data
    :rtype: pynab.models.User
    :param json: json to be parsed to a User object
    :return: user parsed from json
    """
    return User(json["data"]["user"]["id"])


def _parse_budgets(json):
    """
    Product component for factory that creates a list of Budget Summary objects
    from budget summary data
    :rtype: List[pynab.models.BudgetSummary]
    :param json:
    :return: list of budget summaries parsed from json
    """
    return [BudgetSummary(**summary) for summary in json["data"]["budgets"]]


def _parse_budget(json):
    """
    Product component for factory that creates a Budget object from budget data
    :rtype: pynab.models.Budget
    :param json:
    :return: budget parsed from json
    """
    if pynab.requests_session is None:
        # TODO: Decide if a new exception is required here
        raise PynabError("Requests Session should not be none. Please raise an issue on Pynab Github")
    return Budget(pynab.requests_session, **json["data"]["budget"])


def _parse_settings(json):
    """
    Product component for factory that creates a BudgetSettings object from
    budget settings data
    :rtype: pynab.models.Settings
    :param json:
    :return: budget settings parsed from json
    """
    return BudgetSettings(**json["data"]["settings"])


def _parse_transaction(json):
    """
    Product component for factory that creates a Transaction object from
    transaction data
    :rtype: pynab.models.Transaction
    :param json: 
    :return: transaction parsed from json
    """
    return Transaction(**json["data"]["transaction"])


def _parse_transactions(json):
    """
    Product component for factory that creates a list of Transaction objects
    from transaction data
    :rtype: List[pynab.models.Transaction]
    :param json: 
    :return: list of transactions parsed from json
    """
    return [Transaction(**transaction) for transaction in json["data"]["transactions"]]


def _handle_error_response(error):
    """
    Grabs appropriate error from error dictionary based on error response in data
    and raise an exception
    :param error: the error data returned from the YNAB API
    """
    if error["name"] in parse_errors:
        raise parse_errors.get(error["name"])
    else:
        raise PynabError("An unexpected error occurred")
