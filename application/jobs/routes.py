# =================================
#   Job APIs
# =================================
import logging
import sys


from flask import jsonify, request
from flask_restful import Api, Resource

from application.database import db
from application.jobs import job_blueprint
from application.models import Job, UserJob, UserJobRecommendation

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(job_blueprint)


class JobObject(Resource):
    """ This class is used to retrieve all jobs or add a new job """

    def get(self):
        """
        Get All Jobs
        """

        try:
            jobs = Job.query.all()
            serialized_jobs = [job.serialize() for job in jobs]
            return jsonify(serialized_jobs)

        except Exception as ex:
            log.error(ex)

    def post(self):
        """
        Add new job
        """
        data = request.get_json()

        try:
            job = Job(
                title=data['title'],
                job_description=data['jobDescription'],
                level=data['level'],
                date=data['date'],
                start_date=data['startDate'],
                end_date=data['endDate'],
                creator_id=data['creatorId'],
                employment_type=data['employmentType'],
                skills=data['skills']
            )
            db.session.add(job)
            db.session.commit()
            return "job added. job={}".format(job.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400


class HandleJob(Resource):
    """
    This class is used to get job data using job ID or update job data or delete job
    """

    def get(self, job_id):
        """
        Get user
        """
        try:
            job_object = Job.query.filter_by(id=job_id).first()
            serialized_job = job_object.serialize()
            return serialized_job
        except Exception as ex:
            log.info(ex)
            return "job with ID: {} does not exist".format(job_id), 404

    def put(self, job_id):
        """
        Update user data
        """
        data = dict(request.get_json())

        try:
            job_object = Job.query.filter_by(id=job_id)
            job_object.update(data)
            db.session.commit()
            return "job with ID: {} updated".format(job_id)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, job_id):
        """ delete job """
        try:
            job_object = Job.query.filter_by(id=job_id)
            if job_object.first():
                UserJob.query.filter_by(job_id=job_id).delete()
                UserJobRecommendation.query.filter_by(job_id=job_id).delete()
                job_object.delete()
                db.session.commit()
                return "Job with ID: {} deleted".format(job_id)
            else:
                return "Job does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class UserJobApplication(Resource):
    """This class is used to create a user-application for a job """

    def post(self, user_id, job_id):
        """
        Create user-job relationship
        """
        data = request.get_json()

        try:
            user_job = UserJob(
                user_id=user_id,
                job_id=job_id,
                role=data['role'],
                available=data['available'],
                exp_salary=data['expsalary'],
                score=data['score']
            )
            db.session.add(user_job)

            db.session.commit()
            return "relationship for user={} and job={} created".format(user_id, job_id), 201

        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, user_id, job_id):
        """
        delete job application for user and job
        """
        try:
            UserJob.query.filter_by(user_id=user_id, job_id=job_id).delete()
            db.session.commit()
            return "job application for job with ID: {} and user with ID: {} deleted".format(job_id, user_id)
        except Exception as ex:
            log.error(ex)
            return ex


class JobApplication(Resource):
    """This class is used to retrieve all applicants for a job """

    def get(self, job_id):
        """
        retrieve all applicants
        """
        try:
            print(job_id)
            applicants = UserJob.query.filter_by(job_id=job_id)
            print(applicants)
            serialized_applicants = [applicant.serialize() for applicant in applicants]
            return serialized_applicants, 200
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfApplicationsByUser(Resource):
    """Get user's job applications"""

    def get(self, user_id):
        try:
            user_applications = UserJob.query.filter_by(user_id=user_id)
            serialized_applications = [user_application.serialize() for user_application in user_applications]
            return serialized_applications, 200
        except Exception as ex:
            log.error(ex)
            return ex


# Job Routes
api.add_resource(JobObject, '/jobs')
api.add_resource(HandleJob, '/jobs/<job_id>')

api.add_resource(UserJobApplication, '/jobs/<job_id>/apply/<user_id>')
api.add_resource(JobApplication, '/jobs/<job_id>/apply/')
api.add_resource(GetListOfApplicationsByUser, '/users/<user_id>/jobapplies')
