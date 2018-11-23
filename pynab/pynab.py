import requests

from pynab import models


class Pynab:
    base_url = "https://api.youneedabudget.com/v1/"

    def __init__(self, access_token):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {access_token}"
            }
        )

    def __repr__(self):
        return f"Pynab({self.access_token})"

    @property
    def user(self):
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
