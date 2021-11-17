from utils import login
import requests
import unittest


class TestJob(unittest.TestCase):
    student_username = "test_student@test.com"
    student_password = "12345678"

    recruiter_username = "test_recruiter@test.com"
    recruiter_password = "12345678"

    def test(self):
        recr_token, recr_user_id = self.check_login(self.recruiter_username, self.recruiter_password)
        stud_token, stud_user_id = self.check_login(self.student_username, self.student_password)

        self.check_unauthorised_job_creation()
        self.check_unauthorised_job_creation_student(stud_token, stud_user_id)
        job_id = self.check_job_creation_by_recruiter(recr_token, recr_user_id)

        self.check_view_applicants_of_job_unauthorised(job_id, None)
        self.check_view_applicants_of_job_unauthorised(job_id, stud_token)
        self.check_view_applicants_by_owner(job_id, recr_token)

        self.check_unauthorised_job_deletion(job_id, None)
        self.check_unauthorised_job_deletion(job_id, stud_token)
        self.check_job_deletion_by_owner(job_id, recr_token)

    @staticmethod
    def check_login(username, password):
        token, user_id = login(username, password)
        assert (token is not None)
        assert (user_id is not None)
        return token, user_id

    @staticmethod
    def check_unauthorised_job_creation():
        response = TestJob.create_job(None, None)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_unauthorised_job_creation_student(token, user_id):
        response = TestJob.create_job(token, user_id)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_job_creation_by_recruiter(prof_token, prof_user_id):
        response = TestJob.create_job(prof_token, prof_user_id)
        print(response)
        assert (response.status_code == 201)
        print(int(response.text[response.text.index("=")+1:-2]))
        return int(response.text[response.text.index("=")+1:-2])

    @staticmethod
    def check_view_applicants_of_job_unauthorised(job_id, token):
        response = TestJob.view_applicants(job_id, token)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_view_applicants_by_owner(job_id, token):
        response = TestJob.view_applicants(job_id, token)
        print(response)
        assert (response.status_code == 200)

    #
    @staticmethod
    def check_unauthorised_job_deletion(job_id, token):
        response = TestJob.delete_job(job_id, token)
        print(response)
        assert (response.status_code == 401)

    @staticmethod
    def check_job_deletion_by_owner(job_id, token):
        response = TestJob.delete_job(job_id, token)
        print(response)
        assert (response.status_code == 200)

    @staticmethod
    def create_job(token, user_id):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/jobs"
        payload = "{\"title\":\"Machine Learning engineer\",\"employer_id\": 1, \"jobDescription\": \"ML Engineer skilled in Python and Hadoop and R AND SPARK\", \"level\":\"intermediate\", \"date\": \"2020-02-02\", \"startDate\": \"2020-02-02\", \"endDate\": \"2020-02-02\", \"creatorId\": "+str(user_id) + ", \"specialization\": 1, \"country\": \"Greece\", \"state\": \"Attica\", \"city\": \"Athens\", \"employer\": \"Orfium\", \"employmentType\": \"full_time\"}"
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
    def view_applicants(job_id, token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/jobs/"+str(job_id)+"/apply"
        headers = {}
        if token is not None:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
        response = requests.request("GET", url, headers=headers)
        # print(response.text)
        return response

    @staticmethod
    def delete_job(job_id, token):
        url = "http://qualichain.epu.ntua.gr/ntuaAPI5004/jobs/"+str(job_id)
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
