from utils import login
import requests
import unittest


class TestCourse(unittest.TestCase):
    student_username = "test_student@test.com"
    student_password = "12345678"

    professor_username = "test_professor@test.com"
    professor_password = "12345678"

    def test(self):
        prof_token, prof_user_id = self.check_login(self.professor_username, self.professor_password)
        stud_token, stud_user_id = self.check_login(self.student_username, self.student_password)

        self.check_create_course_by_non_professor(stud_token)
        course_id = self.check_create_course_by_professor(prof_token)

        self.check_create_user_course_relation(course_id, prof_user_id, prof_token)

        self.check_others_course_update(course_id, stud_token)
        self.check_own_course_update(course_id, prof_token)

        self.check_others_enrollment_to_course(prof_user_id, stud_token, course_id)

        self.check_own_enrollment_to_course(stud_user_id, stud_token, course_id)

        self.check_delete_course_by_other(stud_token, course_id)
        self.check_delete_course_by_owner(prof_token, course_id)

    @staticmethod
    def check_login(username, password):
        token, user_id = login(username, password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    @staticmethod
    def check_create_course_by_non_professor(stud_token):
        response = TestCourse.create_course(stud_token)
        assert(response.status_code == 401)

    @staticmethod
    def check_create_course_by_professor(prof_token):
        response = TestCourse.create_course(prof_token)
        txt = response.text
        course_id = txt[txt.index('=')+1:-2]
        assert(response.status_code == 201)
        return int(course_id)

    @staticmethod
    def check_create_user_course_relation(course_id, prof_user_id, prof_token):
        response = TestCourse.create_user_course_relation(course_id, prof_user_id, prof_token)
        assert(response.status_code == 201)

    @staticmethod
    def check_delete_course_by_other(other_user_token, course_id):
        response = TestCourse.delete_course(other_user_token, course_id)
        assert (response.status_code == 401)

    @staticmethod
    def check_delete_course_by_owner(owner_token, course_id):
        response = TestCourse.delete_course(owner_token, course_id)
        assert (response.status_code == 200)

    @staticmethod
    def check_others_course_update(course_id, stud_token):
        response = TestCourse.update_course(course_id, stud_token)
        assert (response.status_code == 401)

    @staticmethod
    def check_own_course_update(course_id, prof_token):
        response = TestCourse.update_course(course_id, prof_token)
        assert (response.status_code == 200)

    @staticmethod
    def check_others_enrollment_to_course(stud_user_id, prof_token, course_id):
        response = TestCourse.enroll_user_to_course(stud_user_id, prof_token, course_id)
        assert (response.status_code == 401)

    @staticmethod
    def check_own_enrollment_to_course(stud_user_id, stud_token, course_id):
        response = TestCourse.enroll_user_to_course(stud_user_id, stud_token, course_id)
        assert (response.status_code == 201)

    @staticmethod
    def create_course(token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/courses"
        payload = "{\r\n    \"academic_organisation_id\": null,\r\n        \"description\": \"Significant experience with QualiChain platform\",\r\n        \"end_date\": \"\",\r\n        \"events\": [],\r\n        \"name\": \"QualiChain platform\",\r\n        \"semester\": \"\",\r\n        \"start_date\": \"\",\r\n        \"updatedDate\": \"2021-09-14\"\r\n}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    @staticmethod
    def create_user_course_relation(course_id, prof_user_id, prof_token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/users/" + prof_user_id + '/courses'
        payload = "{\r\n    \"course_id\": \"" + str(course_id) + "\",\r\n    \"course_status\": \"taught\"\r\n}"
        headers = {
            'Authorization': prof_token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    @staticmethod
    def delete_course(token, course_id):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/courses/"+str(course_id)
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers)
        return response

    @staticmethod
    def update_course(course_id, user_token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/courses/" + str(course_id)
        payload = "{\r\n   \"description\": \"updated description\"\r\n}"
        headers = {
            'Authorization': user_token,
            'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        return response

    @staticmethod
    def enroll_user_to_course(user_id, token, course_id):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/users/" + user_id + '/courses'
        payload = "{\r\n    \"course_id\": \"" + str(course_id) + "\",\r\n    \"course_status\": \"enrolled\"\r\n}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response



if __name__ == '__main__':
    unittest.main()
