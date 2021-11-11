from utils import login
import requests
import unittest


class TestProfile(unittest.TestCase):
    username = "test_student@test.com"
    password = "12345678"

    def test(self):
        token, user_id = self.check_login()
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/users/" + user_id

        self.check_own_profile_view(token, url)
        self.check_own_profile_update(token, url)

        other_user_id = '228'
        other_user_url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/users/" + other_user_id
        self.check_others_profile_view(token, other_user_url)

        self.check_others_profile_update(token, other_user_url)

    def check_login(self):
        token, user_id = login(self.username, self.password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    def check_own_profile_view(self, token, user_url):
        response = self.get_user_profile(user_url, token)
        assert(response.status_code == 200)

    def check_others_profile_view(self, token, other_user_url):
        response = self.get_user_profile(other_user_url, token)
        assert (response.status_code == 200)

    def check_own_profile_update(self, token, user_url):
        update_profile_response = self.update_profile(user_url, token)

        assert (update_profile_response == 200)

    def check_others_profile_update(self, token, other_user_url):
        update_profile_response = self.update_profile(other_user_url, token)
        assert (update_profile_response == 401)

    @staticmethod
    def get_user_profile(url, token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)

        return response

    @staticmethod
    def update_profile(url, token):
        payload = "{\"name\": \"test_student1\", \"surname\": \"test_student1\"}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        return response.status_code


if __name__ == '__main__':
    unittest.main()
