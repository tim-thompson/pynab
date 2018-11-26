import requests

import pynab.exceptions
from pynab import models


class Pynab:
    base_url = "https://api.youneedabudget.com/v1/"

    def __init__(self, access_token):
        if access_token is None or len(access_token) == 0:
            raise pynab.exceptions.PynabAuthenticationException(
                "No access token specified"
            )
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    def __repr__(self):
        return f"Pynab({self.access_token})"

    @property
    def user(self):
        """Gets the user id of the currently authenticated user"""
        path = Pynab.base_url + "user"
        response = self.session.get(path)
        return models.PynabFactory.parse(response.json())

    def budgets_summary(self):
        path = Pynab.base_url + "budgets"
        response = self.session.get(path)
        return models.PynabFactory.parse(response.json())

    def budget(self, budget_id):
        path = Pynab.base_url + "budgets/" + budget_id
        response = self.session.get(path)
        return models.PynabFactory.parse(response.json(), budget_id)

    def budget_settings(self, budget_id):
        path = Pynab.base_url + "budgets/" + budget_id + "/settings"
        response = self.session.get(path)
        return models.PynabFactory.parse(response.json(), budget_id)
