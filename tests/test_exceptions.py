import pytest

import pynab.exceptions
from pynab import Pynab, models
from .test_pynab import pynab_vcr, ynab


def test_no_auth_token():
    with pytest.raises(pynab.exceptions.PynabAuthenticationError):
        Pynab("")


@pynab_vcr.use_cassette()
def test_bad_request_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabBadRequestError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_not_authorised_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabAuthenticationError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_subscription_lapsed_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabAccountError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_trial_expired_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabAccountError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_not_found_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabNotFoundError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_resource_not_found_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabNotFoundError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_conflict_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabConflictError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_too_many_requests_exception(ynab):
    """Tests that a rate limit exception is raised when rate limit is exceeded"""
    with pytest.raises(pynab.exceptions.PynabRateLimitExceededError):
        ynab.user()


@pynab_vcr.use_cassette()
def test_internal_server_error_exception(ynab):
    with pytest.raises(pynab.exceptions.PynabInternalServerError):
        ynab.user()
