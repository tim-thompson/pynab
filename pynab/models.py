from dataclasses import dataclass

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


# TODO: Handle iteration error better
def get_from_list(list_search, key, value):
    """Return the first element of a list where the key parameter of the list equals the value parameter."""
    return next(element for element in list_search if getattr(element, key) == value)


def handle_error_response(error):
    if error["name"] == "bad_request":
        raise PynabBadRequestError(
            "YNAB returned a bad request. This is likely a Pynab bug, please report on GitHub"
        )
    elif error["name"] == "unauthorized":
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


@dataclass
class User:
    """Data Class to represent User data returned by YNAB API"""

    id: str


@dataclass
class CurrencyFormat:
    """Data Class to represent Currency Format data returned by YNAB API"""

    iso_code: str
    example_format: str
    decimal_digits: int
    decimal_separator: str
    symbol_first: bool
    group_separator: str
    currency_symbol: str
    display_symbol: str


@dataclass
class Account:
    """Data Class to represent Account data returned by YNAB API"""

    id: str
    name: str
    type: str
    on_budget: bool
    closed: bool
    note: str
    balance: int
    cleared_balance: int
    uncleared_balance: int
    transfer_payee_id: str
    deleted: bool


@dataclass
class Payee:
    """Data Class to represent Payee data returned by YNAB API"""

    id: str
    name: str
    transfer_account_id: str
    deleted: bool


@dataclass
class PayeeLocation:
    """Data Class to represent Payee Location data returned by YNAB API"""

    id: str
    payee_id: str
    latitude: str
    longitude: str
    deleted: bool


@dataclass
class CategoryGroup:
    """Data Class to represent Category Group data returned by YNAB API"""

    id: str
    name: str
    hidden: bool
    deleted: bool


@dataclass
class Category:
    """Data Class to represent Category data returned by YNAB API"""

    id: str
    category_group_id: str
    name: str
    hidden: bool
    original_category_group_id: str
    note: str
    budgeted: int
    activity: int
    balance: int
    goal_type: str
    goal_creation_month: str
    goal_target: int
    goal_target_month: str
    goal_percentage_complete: int
    deleted: bool


@dataclass
class Transaction:
    """Data Class to represent Transaction data returned by YNAB API"""

    id: str
    date: str
    amount: int
    memo: str
    cleared: bool
    approved: bool
    flag_color: str
    account_id: str
    payee_id: str
    category_id: str
    transfer_account_id: str
    transfer_transaction_id: str
    import_id: str
    deleted: bool


@dataclass
class Subtransaction:
    """Data Class to represent Subtransaction data returned from YNAB API"""

    id: str
    transaction_id: str
    amount: int
    memo: str
    payee_id: str
    category_id: str
    transfer_account_id: str
    deleted: bool


@dataclass
class ScheduledTransaction:
    """Data Class to represent Scheduled Transaction Data returned from YNAB API"""

    id: str
    date_first: str
    date_next: str
    frequency: str
    amount: int
    memo: str
    flag_color: str
    account_id: str
    payee_id: str
    category_id: str
    transfer_account_id: str
    deleted: bool


@dataclass
class ScheduledSubtransaction:
    """Data Class to represent Scheduled Subtransaction data returned from YNAB API"""

    id: str
    scheduled_transaction_id: str
    amount: int
    memo: str
    payee_id: str
    category_id: str
    transfer_account_id: str
    deleted: bool


@dataclass
class Month:
    """Data Class to represent Month data returned from YNAB API"""

    month: str
    note: str
    income: int
    budgeted: int
    activity: int
    to_be_budgeted: int
    age_of_money: int
    categories: dict

    def __post_init__(self):
        self.categories = [Category(**category) for category in self.categories]


@dataclass
class BudgetSummary:
    """Data Class to represent Budget Summary data returned from YNAB API"""

    id: str
    name: str
    last_modified_on: str
    date_format: str
    currency_format: CurrencyFormat


class BudgetSettings:
    """Class to represent Budget Settings data returned from YNAB API"""

    def __init__(self, budget_id, **data):
        self.budget_id = budget_id
        self.date_format = data.get("date_format").get("format")
        self.currency_format = CurrencyFormat(**data.get("currency_format"))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.budget_id})"


class Budget:
    """Class to represent Budget data returned from YNAB API"""

    def __init__(self, budget_id, **data):
        self.budget_id = budget_id
        self.name = data.get("name")
        self.last_modified_on = data.get("last_modified_on")
        self.date_format = data.get("date_format").get("format")
        self.currency_format = CurrencyFormat(**data.get("currency_format"))
        self.accounts = [Account(**account) for account in data.get("accounts")]
        self.payees = [Payee(**payee) for payee in data.get("payees")]
        self.payee_locations = [
            PayeeLocation(**payee_location)
            for payee_location in data.get("payee_locations")
        ]
        self.category_groups = [
            CategoryGroup(**category_group)
            for category_group in data.get("category_groups")
        ]
        self.categories = [Category(**category) for category in data.get("categories")]
        self.months = [Month(**month) for month in data.get("months")]
        self.transactions = [
            Transaction(**transaction) for transaction in data.get("transactions")
        ]
        self.subtransactions = [
            Subtransaction(**subtransaction)
            for subtransaction in data.get("subtransactions")
        ]
        self.scheduled_transactions = [
            ScheduledTransaction(**scheduled_transaction)
            for scheduled_transaction in data.get("scheduled_transactions")
        ]
        self.scheduled_subtransactions = [
            ScheduledSubtransaction(**scheduled_subtransaction)
            for scheduled_subtransaction in data.get("scheduled_subtransactions")
        ]

    def account(self, account_id):
        return get_from_list(self.accounts, "id", account_id)

    def category(self, category_id):
        return get_from_list(self.categories, "id", category_id)

    def update_category(self, category):
        pass

    def payee(self, payee_id):
        return get_from_list(self.payees, "id", payee_id)

    def payee_location(self, payee_location_id):
        return get_from_list(self.payee_locations, "id", payee_location_id)

    def month(self, month):
        return get_from_list(self.months, "month", month)

    def transaction(self, transaction_id):
        return get_from_list(self.transactions, "id", transaction_id)

    def new_transaction(self):
        pass

    def update_transaction(self, transaction):
        pass

    def scheduled_transaction(self, scheduled_transaction_id):
        return get_from_list(
            self.scheduled_transactions, "id", scheduled_transaction_id
        )
