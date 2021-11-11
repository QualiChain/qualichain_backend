from utils import login
import requests
import json
import unittest


class TestCV(unittest.TestCase):
    username = "test_student@test.com"
    password = "12345678"

    def test(self):
        token, user_id = self.check_login()
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/CV/" + user_id

        self.check_own_cv_creation(token, url)

        self.check_own_cv_deletion(token, url)

        other_user_id = '228'
        other_user_url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/CV/" + other_user_id
        self.check_others_cv_view(token, other_user_url)

        self.check_others_cv_creation(token, other_user_url)

        self.check_others_cv_deletion(token, other_user_url)

    def check_login(self):
        token, user_id = login(self.username, self.password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    def check_own_cv_creation(self, token, url):
        create_cv_response = self.create_cv(url, token)
        assert (create_cv_response.status_code == 201)
        cv = json.loads(self.get_user_cv(url, token).text)
        assert (len(cv) == 1)
        cv_description = cv[0]['description']
        assert (cv_description == 'some description')

    def check_own_cv_deletion(self, token, url):
        delete_status = self.delete_cv(url, token)
        assert (delete_status == 200)
        cv = json.loads(self.get_user_cv(url, token).text)
        assert (len(cv) == 0)

    def check_others_cv_view(self, token, other_user_url):
        response = self.get_user_cv(other_user_url, token)
        assert(response.status_code == 401)

    def check_others_cv_creation(self, token, other_user_url):
        create_cv_response = self.create_cv(other_user_url, token)
        assert (create_cv_response.status_code == 401)

    def check_others_cv_deletion(self, token, other_user_url):
        delete_status = self.delete_cv(other_user_url, token)
        assert (delete_status == 401)

    @staticmethod
    def create_cv(url, token):
        payload = "{\n\"targetSector\": \"Software Engineering\",\n\"Description\": \"some description\",\n\"workHistory\": [{\n    \"name\":\"workA\"\n    }],\"Education\": [{\n        \"name\":\"educationA\"}],\n        \"skills\": [{\"id\":1, \"name\":\"Algebra\", \"skill_level\":\"1\"}]\n}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        return response

    @staticmethod
    def get_user_cv(url, token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)

        return response

    @staticmethod
    def delete_cv(url, token):
        payload = {}
        headers = {
            'Authorization': token
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)
        return response.status_code


if __name__ == '__main__':
    unittest.main()
