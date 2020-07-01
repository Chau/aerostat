import requests


class Api():

    def login(self):
        url = '{}user/login?_format=json'.format(self.api_url)
        response = requests.post(url, json={'name': name, 'pass': password})
