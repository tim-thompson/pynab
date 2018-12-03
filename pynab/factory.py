from pynab.models import User, BudgetSummary, Budget, BudgetSettings

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


class PynabFactory:
    @staticmethod
    def parse(json, budget_id=None):
        if "error" in json:
            handle_error_response(json["error"])
        elif "user" in json["data"]:
            return User(json["data"]["user"]["id"])
        elif "budgets" in json["data"]:
            return [BudgetSummary(**summary) for summary in json["data"]["budgets"]]
        elif "budget" in json["data"]:
            return Budget(budget_id, **json["data"]["budget"])
        elif "settings" in json["data"] and budget_id is not None:
            return BudgetSettings(budget_id, **json["data"]["settings"])


def handle_error_response(error):
    if error["name"] == "bad_request":
        raise PynabBadRequestError(
            "YNAB returned a bad request. This is likely a Pynab bug, please report on GitHub"
        )
    elif error["name"] == "not_authorized":
        raise PynabAuthenticationError("Authentication with access token failed")
    elif error["name"] == "subscription_lapsed":
        raise PynabAccountError(
            "Subscription lapsed, API access requires an active subscription or trial"
        )
    elif error["name"] == "trial_expired":
        raise PynabAccountError(
            "Trial expired, API access requires an active subscription or trial"
        )
    elif error["name"] == "not_found":
        raise PynabNotFoundError(
            "URI not found. This is likely a Pynab bug, please report on GitHub"
        )
    elif error["name"] == "resource_not_found":
        raise PynabNotFoundError("Requested resource not found")
    elif error["name"] == "conflict":
        raise PynabConflictError(
            "Could not complete operation, conflict with existing resource"
        )
    elif error["name"] == "too_many_requests":
        raise PynabRateLimitExceededError("Rate limit exceeded, too many requests")
    elif error["name"] == "internal_server_error":
        raise PynabInternalServerError(
            "An internal server error occurred. This is a YNAB problem, try again later"
        )
    raise PynabError("An unexpected error occurred")
