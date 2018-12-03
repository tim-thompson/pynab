import requests

import pynab.exceptions
from pynab import models
from pynab.exceptions import PynabConnectionError


class Pynab:
    base_url = "https://api.youneedabudget.com/v1/"

    def __init__(self, access_token: str):
        if access_token is None or len(access_token) == 0:
            raise pynab.exceptions.PynabAuthenticationError("No access token specified")
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    def __repr__(self):
        return f"Pynab({self.access_token})"

    @property
    def user(self):
        """Gets information about the currently authenticated user

        :rtype: :class:`pynab.models.User`
        :return: a user object of the currently authenticated user
        """
        path = Pynab.base_url + "user"
        try:
            response = self.session.get(path)
        except requests.exceptions.ConnectionError:
            raise PynabConnectionError
        return models.PynabFactory.parse(response.json())

    def budgets_summary(self):
        """Gets a list containing a limited subset of information from each budget.
        Should be used to retrieve budget IDs to make further requests.

        :rtype: List[pynab.models.BudgetSummary]
        :return: a list containing summary information of each budget
        """
        path = Pynab.base_url + "budgets"
        response = self.session.get(path)
        return models.PynabFactory.parse(response.json())

    def budget(self, budget_id):
        """Gets a single budget by id

        :rtype: pynab.models.Budget
        :param budget_id: the UUID of the budget that should be returned
        :return: a new budget object
        """
        path = Pynab.base_url + "budgets/" + budget_id
        response = self.session.get(path)
        return models.PynabFactory.parse(response.json(), budget_id)

    def budget_settings(self, budget_id):
        """Gets the settings for a single budget by id

        :rtype: pynab.models.BudgetSettings
        :param budget_id: the UUID of the budget that contains the settings to be retrieved
        :return: a new budget settings object
        """
        path = Pynab.base_url + "budgets/" + budget_id + "/settings"
        response = self.session.get(path)
        return models.PynabFactory.parse(response.json(), budget_id)
