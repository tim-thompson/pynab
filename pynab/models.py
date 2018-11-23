from collections import namedtuple


class PynabException(Exception):
    """Base exception class for Pynab"""

    pass


class PynabAuthenticationException(PynabException):
    """Exception raised for authentication errors in a request"""

    pass


class PynabResourceDoesNotExist(PynabException):
    pass


class PynabFactory:
    def __init__(self):
        pass

    @staticmethod
    def parse(json, budget_id=None):
        if "error" in json:
            raise PynabException
        elif "user" in json["data"]:
            return User(id=json["data"]["user"]["id"])
        elif "budgets" in json["data"]:
            return [BudgetSummary(**summary) for summary in json["data"]["budgets"]]
        elif "budget" in json["data"]:
            return Budget(budget_id, **json["data"]["budget"])
        elif "settings" in json["data"] and budget_id is not None:
            return BudgetSettings(budget_id, **json["data"]["settings"])


class User:
    def __init__(self, **data):
        self.user_id = data.get("id")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.user_id})"


CurrencyFormat = namedtuple(
    "CurrencyFormat",
    [
        "iso_code",
        "example_format",
        "decimal_digits",
        "decimal_separator",
        "symbol_first",
        "group_separator",
        "currency_symbol",
        "display_symbol",
    ],
)
Account = namedtuple(
    "Account",
    [
        "id",
        "name",
        "type",
        "on_budget",
        "closed",
        "note",
        "balance",
        "cleared_balance",
        "uncleared_balance",
        "transfer_payee_id",
        "deleted",
    ],
)
Payee = namedtuple("Payee", ["id", "name", "transfer_account_id", "deleted"])
PayeeLocation = namedtuple(
    "PayeeLocation", ["id", "payee_id", "latitude", "longitude", "deleted"]
)
CategoryGroup = namedtuple("CategoryGroup", ["id", "name", "hidden", "deleted"])
Category = namedtuple(
    "Category",
    [
        "id",
        "category_group_id",
        "name",
        "hidden",
        "original_category_group_id",
        "note",
        "budgeted",
        "activity",
        "balance",
        "goal_type",
        "goal_creation_month",
        "goal_target",
        "goal_target_month",
        "goal_percentage_complete",
        "deleted",
    ],
)
Transaction = namedtuple(
    "Transaction",
    [
        "id",
        "date",
        "amount",
        "memo",
        "cleared",
        "approved",
        "flag_color",
        "account_id",
        "payee_id",
        "category_id",
        "transfer_account_id",
        "transfer_transaction_id",
        "import_id",
        "deleted",
    ],
)
Subtransaction = namedtuple(
    "Subtransaction",
    [
        "id",
        "transaction_id",
        "amount",
        "memo",
        "payee_id",
        "category_id",
        "transfer_account_id",
        "deleted",
    ],
)
ScheduledTransaction = namedtuple(
    "ScheduledTransaction",
    [
        "id",
        "date_first",
        "date_next",
        "frequency",
        "amount",
        "memo",
        "flag_color",
        "account_id",
        "payee_id",
        "category_id",
        "transfer_account_id",
        "deleted",
    ],
)
ScheduledSubtransaction = namedtuple(
    "ScheduledSubtransaction",
    [
        "id",
        "scheduled_transaction_id",
        "amount",
        "memo",
        "payee_id",
        "category_id",
        "transfer_account_id",
        "deleted",
    ],
)


class Month:
    def __init__(
        self,
        month,
        note,
        income,
        budgeted,
        activity,
        to_be_budgeted,
        age_of_money,
        categories,
    ):
        self.month = month
        self.note = note
        self.income = income
        self.budgeted = budgeted
        self.activity = activity
        self.to_be_budgeted = to_be_budgeted
        self.age_of_money = age_of_money
        self.categories = [Category(**category) for category in categories]


class Budget:
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
        account = [account for account in self.accounts if account.id == account_id]
        if len(account) == 0:
            raise PynabResourceDoesNotExist()
        return account

    def category(self, category_id):
        pass

    def update_category(self, category):
        pass

    def payee(self, payee_id):
        pass

    def payee_location(self, payee_location_id):
        pass

    def month(self, month):
        pass

    def new_transaction(self):
        pass

    def update_transaction(self, transaction):
        pass

    def scheduled_transaction(self, scheduled_transaction_id):
        pass


class BudgetSummary:
    def __init__(self, **data):
        self.id = data.get("id")
        self.name = data.get("name")
        self.last_modified_on = data.get("last_modified_on")
        self.date_format = data.get("date_format").get("format")
        self.currency_format = CurrencyFormat(**data.get("currency_format"))


class BudgetSettings:
    def __init__(self, budget_id, **data):
        self.budget_id = budget_id
        self.date_format = data.get("date_format").get("format")
        self.currency_format = CurrencyFormat(**data.get("currency_format"))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.budget_id})"
