from utils import login
import requests
import unittest


class TestCourseRecommendation(unittest.TestCase):
    student_username = "test_student@test.com"
    student_password = "12345678"

    def test(self):
        stud_token, stud_user_id = self.check_login(self.student_username, self.student_password)

        self.check_unauthorised_user()
        self.check_authorised_student(stud_token)

    @staticmethod
    def check_login(username, password):
        token, user_id = login(username, password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    @staticmethod
    def check_unauthorised_user():
        response = TestCourseRecommendation.get_course_recommendations(None)
        # print(response)
        assert(response.status_code == 401)

    @staticmethod
    def check_authorised_student(token):
        response = TestCourseRecommendation.get_course_recommendations(token)
        assert (response.status_code == 200)


    @staticmethod
    def get_course_recommendations(token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/recommend"
        payload = "{\"source\":{\"PersonURI\":\":18\",\"Label\":\"Updated service Test CV\",\"targetSector\":\"IT\",\"expectedSalary\":\"\",\"Description\":\"Making my first CV\",\"skills\":[{\"label\":\"ca\",\"comment\":\"Skill comment 8\",\"proficiencyLevel\":\"basic\",\"uri\":\":id4d746106-b2bb-4ef7-a35c-297bf145acf5\"}, {\"label\":\"c\",\"comment\":\"Skill comment 8\",\"proficiencyLevel\":\"basic\",\"uri\":\":id4d746106-b2bb-4ef7-a35c-297bf145acf5\"}],\"workHistory\":[{\"title\":\"Cashier\",\"from\":\"2010-05-15\",\"to\":\"2012-12-31\",\"organisation\":\"Generic Groceries store\",\"description\":\"\"}],\"Education\":[{\"from\":\"2013-10-15\",\"to\":\"2018-07-15\",\"description\":\"Computer science\"}]},\"source_type\":\"cv\",\"recommendation_type\":\"courses\"}"
        headers = {}
        if token is not None:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        return response


if __name__ == '__main__':
    unittest.main()
