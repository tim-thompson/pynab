import json
from dataclasses import dataclass

import pynab
import pynab.exceptions
import pynab.factory


def get_from_list(list_search, key, value):
    """Return the first element of a list where the key parameter
    of the list equals the value parameter.
    """
    # TODO: Handle iteration error better
    return next(element for element in list_search if getattr(element, key) == value)


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
class NewTransaction:
    """Data Class to represent new transactions created by the user"""

    account_id: str
    date: str
    amount: int
    memo: str = None
    cleared: str = None
    approved: bool = None
    flag_color: str = None
    payee_id: str = None
    category_id: str = None
    transfer_account_id: str = None
    transfer_transaction_id: str = None
    matched_transaction_id: str = None
    import_id: str = None
    deleted: bool = None

    def __post_init__(self):
        if self.account_id in {None, ""} or self.amount in {None, ""} or self.date in {None, ""}:
            print("post init")
            raise pynab.exceptions.PynabError(
                "Please provide a valid value for each mandatory field: account_id, date, amount"
            )


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
    matched_transaction_id: str = None
    account_name: str = None
    payee_name: str = None
    category_name: str = None
    subtransactions: dict = None

    def __post_init__(self):
        if self.subtransactions is not None:
            self.subtransactions = [Subtransaction(**subtransaction) for subtransaction in self.subtransactions]


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
    deleted: bool = None

    def __post_init__(self):
        self.categories = [Category(**category) for category in self.categories]


@dataclass
class BudgetSummary:
    """Data Class to represent Budget Summary data returned from YNAB API"""

    id: str
    name: str
    last_modified_on: str
    date_format: dict
    currency_format: CurrencyFormat
    first_month: str = None
    last_month: str = None

    def __post_init__(self):
        self.date_format = self.date_format.get("format")


class BudgetSettings:
    """Class to represent Budget Settings data returned from YNAB API"""

    def __init__(self, **data):
        self.date_format = data.get("date_format").get("format")
        self.currency_format = CurrencyFormat(**data.get("currency_format"))

    def __repr__(self):
        return f"{self.__class__.__name__}"


class Budget:
    """Class to represent Budget data returned from YNAB API"""

    def __init__(self, requests_session, **data):
        self.budget_id = data.get("id")
        self.session = requests_session
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

    def account(self, account_id: str):
        """Gets a single account by account id

        :rtype: pynab.models.Account
        :param account_id: the UUID of the account to be retrieved
        :return: a new account object
        """
        return get_from_list(self.accounts, "id", account_id)

    def category(self, category_id: str):
        """Gets a single category by category id

        :rtype: pynab.models.Category
        :param category_id: the UUID of the category to be retrieved
        :return: a new category object
        """
        return get_from_list(self.categories, "id", category_id)

    def update_category(self, category: str):
        # TODO: finish implementation
        pass

    def payee(self, payee_id: str):
        """Gets a single payee by payee id

        :rtype: pynab.models.Payee
        :param payee_id: the UUID of the payee to be retrieved
        :return: a new payee object
        """
        return get_from_list(self.payees, "id", payee_id)

    def payee_location(self, payee_location_id: str):
        """Gets a single payee location by payee location id

        :rtype: pynab.models.PayeeLocation
        :param payee_location_id: the UUID of the payee location to be retrieved
        :return: a new payee location object
        """
        return get_from_list(self.payee_locations, "id", payee_location_id)

    def month(self, month: str):
        """Gets a single month by month id

        :rtype: pynab.models.Month
        :param month: the month to be returned
        :return: a new month object
        """
        return get_from_list(self.months, "month", month)

    def transaction(self, transaction_id: str):
        """Gets a single transaction by transaction id

        :rtype: pynab.models.Transaction
        :param transaction_id: the UUID of the transaction to be retrieved
        :return: a new transaction object
        """
        return get_from_list(self.transactions, "id", transaction_id)

    def create_transactions(self, new_transactions):
        """Creates one or more transactions within a budget

        :rtype: List[pynab.models.NewTransaction]
        :param new_transactions: list of dicts representing each transaction
        :return: a list of all transactions created
        """
        if new_transactions is None or len(new_transactions) == 0:
            # TODO: Create proper exception for this
            raise pynab.exceptions.PynabError

        path = f"{pynab.Pynab._base_url}/budgets/{self.budget_id}/transactions"
        data = {
            "transactions": [
                new_transaction.__dict__ for new_transaction in new_transactions
            ]
        }
        print(data)
        response = self.session.post(path, json=data)
        return pynab.factory.PynabFactory.parse(response.json(), self.budget_id)

    def update_transaction(self, transaction):
        # TODO: complete implementation
        pass

    def scheduled_transaction(self, scheduled_transaction_id: str):
        """Gets a single scheduled transaction by scheduled transaction id

        :rtype: pynab.models.ScheduledTransaction
        :param scheduled_transaction_id: the UUID of the scheduled transaction to be retrieved
        :return: a new scheduled transaction object
        """
        return get_from_list(
            self.scheduled_transactions, "id", scheduled_transaction_id
        )
