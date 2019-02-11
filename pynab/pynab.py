import requests

from pynab.factory import PynabFactory
from pynab.exceptions import PynabAuthenticationError, PynabConnectionError, PynabError


class Pynab:
    _base_url = "https://api.youneedabudget.com/v1"

    def __init__(self, access_token: str):
        if access_token is None or len(access_token) == 0:
            raise PynabAuthenticationError("No access token specified")
        self._access_token = access_token
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {access_token}"})
        self._factory = PynabFactory(self._session)

    def __repr__(self):
        return f"Pynab(User ID: {self._access_token})"

    @property
    def user(self):
        """Gets information about the currently authenticated user

        :rtype: pynab.models.User
        :return: a user object of the currently authenticated user
        """
        path = f"{self._base_url}/user"
        try:
            response = self._session.get(path)
        except requests.exceptions.ConnectionError:
            raise PynabConnectionError
        return self._factory.parse(response.json())

    def budgets_list(self):
        """Gets a list containing a limited subset of information from each budget.
        Should be used to retrieve budget IDs to make further requests.

        :rtype: List[pynab.models.BudgetSummary]
        :return: a list containing summary information of each budget
        """
        path = f"{self._base_url}/budgets"
        response = self._session.get(path)
        return self._factory.parse(response.json())

    def budget(self, budget_id):
        """Gets a single budget by id

        :rtype: pynab.models.Budget
        :param budget_id: the UUID of the budget that should be returned
        :return: a new budget object
        """
        path = f"{self._base_url}/budgets/{budget_id}"
        response = self._session.get(path)
        return self._factory.parse(response.json())

    def budget_settings(self, budget_id):
        """Gets the settings for a single budget by id

        :rtype: pynab.models.BudgetSettings
        :param budget_id: the UUID of the budget that contains the settings to be retrieved
        :return: a new budget settings object
        """
        path = f"{self._base_url}/budgets/{budget_id}/settings"
        response = self._session.get(path)
        return self._factory.parse(response.json())
