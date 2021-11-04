from utils import login
import requests
import unittest


class TestCurriculumDesign(unittest.TestCase):
    student_username = "test_student@test.com"
    student_password = "12345678"

    professor_username = "test_professor@test.com"
    professor_password = "12345678"

    def test(self):
        prof_token, prof_user_id = self.check_login(self.professor_username, self.professor_password)
        stud_token, stud_user_id = self.check_login(self.student_username, self.student_password)

        self.check_unauthorised_user()
        self.check_authorised_student(stud_token)
        self.check_authorised_professor(prof_token)

    @staticmethod
    def check_login(username, password):
        token, user_id = login(username, password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    @staticmethod
    def check_unauthorised_user():
        response = TestCurriculumDesign.get_curriculum_design_recommendations(None)
        print(response)
        assert(response.status_code == 401)

    @staticmethod
    def check_authorised_student(token):
        response = TestCurriculumDesign.get_curriculum_design_recommendations(token)
        assert (response.status_code == 401)

    @staticmethod
    def check_authorised_professor(token):
        response = TestCurriculumDesign.get_curriculum_design_recommendations(token)
        assert (response.status_code == 200)

    @staticmethod
    def get_curriculum_design_recommendations(token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/curriculum_design"
        payload = {}
        headers = {}
        if token is not None:
            headers = {
                'Authorization': token
            }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response


if __name__ == '__main__':
    unittest.main()
