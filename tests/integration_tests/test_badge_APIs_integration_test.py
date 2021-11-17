from utils import login
import requests
import unittest


class TestBadge(unittest.TestCase):
    student_username = "test_student@test.com"
    student_password = "12345678"

    professor_username = "test_professor@test.com"
    professor_password = "12345678"

    def test(self):
        prof_token, prof_user_id = self.check_login(self.professor_username, self.professor_password)
        stud_token, stud_user_id = self.check_login(self.student_username, self.student_password)

        self.check_create_badge_unauthorised()
        badge_id = self.check_create_badge(stud_token)

        self.check_award_badge_unauthorised(badge_id, stud_user_id)
        self.check_award_badge(badge_id, stud_user_id, prof_token)

    @staticmethod
    def check_login(username, password):
        token, user_id = login(username, password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    @staticmethod
    def check_create_badge_unauthorised():
        response = TestBadge.create_badge(None)
        assert(response.status_code == 401)

    @staticmethod
    def check_create_badge(token):
        response = TestBadge.create_badge(token)
        txt = response.text
        badge_id = txt[txt.index('=')+1:-10]
        assert(response.status_code == 201)
        return int(badge_id)

    @staticmethod
    def check_award_badge_unauthorised(badge_id, user_id):
        response = TestBadge.award_badge(None, badge_id, user_id)
        assert (response.status_code == 401)

    @staticmethod
    def check_award_badge(badge_id, user_id, token):
        response = TestBadge.award_badge(token, badge_id, user_id)
        print(response)
        assert (response.status_code == 201)

    @staticmethod
    def create_badge(token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/badges"
        payload = """{"type":"Undergraduate","oubadge":{"@context":["https://w3id.org/openbadges/v2",{"@vocab":"https://blockchain.open.ac.uk/vocab/"}],"type":"BadgeClass","name":"Smart Badge For continuous integration and testing","description":"Smart Badge For continuous integration and testing","image":"https://pngimg.com/image/60258","version":"1","criteria":{"type":"Criteria","narrative":"The holder of this badge has demonstrated the specified skills","skills":"testing, CI"},"issuer":{"type":"Issuer","name":"Vagelis Karakolis Professor","description":"Professor","email":"vk_professor@epu.ntua.gr"}}}"""
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    @staticmethod
    def award_badge(token, badge_id, user_id):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/user/awards"
        payload = """{"badge_id":"""+str(badge_id)+""", "user_id": """+ str(user_id) +""", "oubadge_user":""} """
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response


if __name__ == '__main__':
    unittest.main()
