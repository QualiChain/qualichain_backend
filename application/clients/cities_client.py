import requests

from application.settings import API_TOKEN, MAIL_USERNAME, UNIVERSAL_URLS


class CitiesClient(object):
    def __init__(self):
        self.api_token = API_TOKEN
        self.user_email = MAIL_USERNAME
        self.auth_token = self.get_auth_token()

    def get_auth_token(self):
        """This function is used to fetch auth-token"""

        headers = {
            'Accept': 'application/json',
            'api-token': API_TOKEN,
            'user-email': 'qualichain@gmail.com'
        }
        response = requests.get(
            url=UNIVERSAL_URLS['AUTH'],
            headers=headers
        )

        json_response = response.json()
        auth_token = json_response['auth_token']
        return auth_token

    def get_countries(self):
        """This function is used to retrieve auth tokens"""

        headers = {"Authorization": "Bearer {}".format(self.auth_token)}
        response = requests.get(
            url=UNIVERSAL_URLS['COUNTRIES'],
            headers=headers
        )
        return response

    def get_country_states(self, country):
        """This function is used to fetch country states"""

        headers = {"Authorization": "Bearer {}".format(self.auth_token)}
        response = requests.get(
            url="{}/{}".format(UNIVERSAL_URLS['STATES'], country),
            headers=headers
        )
        return response

    def get_state_cities(self, state):
        """This function is used to fetch state cities"""

        headers = {"Authorization": "Bearer {}".format(self.auth_token)}
        response = requests.get(
            url="{}/{}".format(UNIVERSAL_URLS['CITIES'], state),
            headers=headers
        )
        return response
