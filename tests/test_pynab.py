# tests/test_pynab.py
import pytest
import vcr

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


@pynab_vcr.use_cassette()
def test_user_info(ynab):
    """Tests an API call to get information about authenticated user"""
    assert ynab.user.user_id == "string"


@pynab_vcr.use_cassette()
def test_budgets_summary_list(ynab):
    """Tests an API call to get a summary list of all budgets"""
    budgets_summary = ynab.budgets_summary()

    assert isinstance(budgets_summary, list)


@pynab_vcr.use_cassette()
def test_get_single_budget_full(ynab):
    """Tests an API call to get a full budget export of a single budget by ID"""
    budget = ynab.budget("string")
    print(budget.accounts)
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
