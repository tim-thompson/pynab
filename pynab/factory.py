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

errors = {
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


class PynabFactory:
    def __init__(self, requests_session):
        self.requests_session = requests_session

    def parse(self, json):
        if "error" in json:
            _handle_error_response(json["error"])

        parser = self._get_parser(json["data"])
        return parser(json)

    def _get_parser(self, data_type):
        if "user" in data_type:
            return self._parse_user
        elif "budgets" in data_type:
            return self._parse_budgets
        elif "budget" in data_type:
            return self._parse_budget
        elif "settings" in data_type:
            return self._parse_settings
        elif "transaction" in data_type:
            return self._parse_transaction
        elif "transactions" in data_type:
            return self._parse_transactions
        else:
            # TODO: Create proper exception
            raise PynabError("Unable to parse response from YNAB API")

    def _parse_user(self, json):
        return User(json["data"]["user"]["id"])

    def _parse_budgets(self, json):
        return [BudgetSummary(**summary) for summary in json["data"]["budgets"]]

    def _parse_budget(self, json):
        if self.requests_session is None:
            # TODO: Decide if a new exception is required here
            raise PynabError("Requests Session should not be none. Please raise an issue on Pynab Github")
        return Budget(self.requests_session, **json["data"]["budget"])

    def _parse_settings(self, json):
        return BudgetSettings(**json["data"]["settings"])

    def _parse_transaction(self, json):
        return Transaction(**json["data"]["transaction"])

    def _parse_transactions(self, json):
        return [Transaction(**transaction) for transaction in json["data"]["transactions"]]

def _handle_error_response(error):
    if error["name"] in errors:
        raise errors.get(error["name"])
    else:
        raise PynabError("An unexpected error occurred")
