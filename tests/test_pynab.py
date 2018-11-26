# tests/test_pynab.py
import pytest
import vcr

import pynab.exceptions
from pynab import Pynab, models

pynab_vcr = vcr.VCR(
    serializer="yaml",
    decode_compressed_response=True,
    cassette_library_dir="cassettes",
    filter_headers=["authorization"],
)


@pytest.fixture
def ynab():
    """Setup an instance of Pynab"""
    ynab = Pynab("auth_token")
    return ynab


def test_no_auth_token():
    with pytest.raises(pynab.exceptions.PynabAuthenticationError):
        ynab = Pynab("")


@pynab_vcr.use_cassette()
def test_user_info(ynab):
    """Tests an API call to get information about authenticated user"""
    assert ynab.user.id == "string"


@pynab_vcr.use_cassette()
def test_budgets_summary_list(ynab):
    """Tests an API call to get a summary list of all budgets"""
    budgets_summary = ynab.budgets_summary()

    assert isinstance(budgets_summary, list)


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_single_budget_full(ynab):
    """Tests an API call to get a full budget export of a single budget by ID"""
    budget = ynab.budget("string")
    assert isinstance(budget, models.Budget)


@pynab_vcr.use_cassette()
def test_get_single_budget_settings(ynab):
    """Tests an API call to get the settings for a budget by ID"""
    settings = ynab.budget_settings("string")

    assert isinstance(settings, models.BudgetSettings)
    assert settings.currency_format.currency_symbol == "string"
    assert settings.date_format == "string"
    assert settings.currency_format.decimal_digits == 0
    assert settings.currency_format.display_symbol is True


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_account_by_account_id_from_budget(ynab):
    """Tests that an account can be retrieved from a Budget object by ID"""
    budget = ynab.budget("string")
    account = budget.account("string")
    assert isinstance(account, models.Account)
    assert account.id == "string"


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_category_by_category_id_from_budget(ynab):
    """Tests that a category can be retrieved from a Budget object by ID"""
    budget = ynab.budget("string")
    category = budget.category("string")
    assert isinstance(category, models.Category)
    assert category.id == "string"


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_payee_by_payee_id_from_budget(ynab):
    """Tests that a payee can be retrieved from a Budget object by ID"""
    budget = ynab.budget("string")
    payee = budget.payee("string")
    assert isinstance(payee, models.Payee)
    assert payee.id == "string"


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_payee_location_by_payee_location_id_from_budget(ynab):
    """Tests that a payee location can be retrieved from a Budget object by ID"""
    budget = ynab.budget("string")
    payee_location = budget.payee_location("string")
    assert isinstance(payee_location, models.PayeeLocation)
    assert payee_location.id == "string"


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_month_by_month_from_budget(ynab):
    """Tests that a month can be retrieved from a Budget object by ID"""
    budget = ynab.budget("string")
    month = budget.month("string")
    assert isinstance(month, models.Month)
    assert month.month == "string"


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_transaction_by_transaction_id_from_budget(ynab):
    """Tests that a transaction can be retrieved from a Budget object by ID"""
    budget = ynab.budget("string")
    transaction = budget.transaction("string")
    assert isinstance(transaction, models.Transaction)
    assert transaction.id == "string"


@pynab_vcr.use_cassette("cassettes/test_full_budget")
def test_get_scheduled_transaction_by_scheduled_transaction_id_from_budget(ynab):
    """Tests that a scheduled transaction can be retrieved from a Budget object by ID"""
    budget = ynab.budget("string")
    scheduled_transaction = budget.scheduled_transaction("string")
    assert isinstance(scheduled_transaction, models.ScheduledTransaction)
    assert scheduled_transaction.id == "string"


@pynab_vcr.use_cassette()
def test_rate_limit_exceeded(ynab):
    """Tests that a rate limit exception is raised when rate limit is exceeded"""
    with pytest.raises(pynab.exceptions.PynabRateLimitExceededError):
        budget = ynab.user
