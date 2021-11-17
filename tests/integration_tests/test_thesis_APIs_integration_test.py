from utils import login
import requests
import unittest


class TestThesis(unittest.TestCase):
    student_username = "test_student@test.com"
    student_password = "12345678"

    professor_username = "test_professor@test.com"
    professor_password = "12345678"

    def test(self):
        prof_token, prof_user_id = self.check_login(self.professor_username, self.professor_password)
        stud_token, stud_user_id = self.check_login(self.student_username, self.student_password)

        self.check_unauthorised_thesis_creation()
        self.check_unauthorised_thesis_creation_student(stud_token, stud_user_id)
        thesis_id = self.check_thesis_creation_by_professor(prof_token, prof_user_id)

        self.check_unauthorised_thesis_deletion(thesis_id)
        self.check_unauthorised_thesis_deletion_student(thesis_id, stud_token)
        self.check_thesis_deletion_professor(thesis_id, prof_token)

    @staticmethod
    def check_login(username, password):
        token, user_id = login(username, password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    @staticmethod
    def check_unauthorised_thesis_creation():
        response = TestThesis.create_thesis(None, None)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_unauthorised_thesis_creation_student(token, user_id):
        response = TestThesis.create_thesis(token, user_id)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_thesis_creation_by_professor(prof_token, prof_user_id):
        response = TestThesis.create_thesis(prof_token, prof_user_id)
        print(response)
        assert (response.status_code == 201)
        return int(response.text[response.text.index("=")+1:-2])

    @staticmethod
    def check_unauthorised_thesis_deletion(thesis_id):
        response = TestThesis.delete_thesis(thesis_id, None)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_unauthorised_thesis_deletion_student(thesis_id, token):
        response = TestThesis.delete_thesis(thesis_id, token)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_thesis_deletion_professor(thesis_id, token):
        response = TestThesis.delete_thesis(thesis_id, token)
        print(response)
        assert (response.status_code == 200)

    @staticmethod
    def create_thesis(token, user_id):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/thesis"
        payload = "{\"title\":\"Applications of Reinforcement Learning\",\"professor_id\":" + str(user_id) + ",\"description\":\"Applications of Reinforcement Learning\"}"
        headers = {}
        if token is not None:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        return response

    @staticmethod
    def delete_thesis(thesis_id, token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/thesis/"+str(thesis_id)
        headers = {}
        if token is not None:
            headers = {
                'Authorization': token
            }
        response = requests.request("DELETE", url, headers=headers)
        # print(response.text)
        return response


if __name__ == '__main__':
    unittest.main()
