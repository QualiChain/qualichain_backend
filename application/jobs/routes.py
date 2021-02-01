# =================================
#   Job APIs
# =================================
import logging
import sys

from flask import jsonify, request
from flask_restful import Api, Resource

from application.clients.cities_client import CitiesClient
from application.clients.qualichain_analyzer import QualiChainAnalyzer
from application.database import db
from application.jobs import job_blueprint
from application.models import Job, UserJobRecommendation, JobSkill, UserApplication, Skill, Specialization
from application.decorators import only_profile_owner, only_recruiters_and_profile_owners, only_lifelong_learner, \
    only_authenticated, only_recruiters_and_recruitment_organizations, only_recruiter_creator_of_job

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(job_blueprint)
analyzer = QualiChainAnalyzer()


class JobObject(Resource):
    """ This class is used to retrieve all jobs or add a new job """

    # method_decorators = {'post': [only_recruiters_and_recruitment_organizations], 'get': [only_authenticated]}

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
        data = dict(request.get_json())
        data['required_skills'] = []

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
                employer=data['employer'],
                specialization_id=data['specialization'],
                country=data['country'],
                state=data['state'],
                city=data['city']
            )
            db.session.add(job)
            db.session.commit()

            if 'skills' in data.keys():
                for skill in data['skills']:
                    data['required_skills'].append(skill["name"])

                    skill_job = JobSkill(
                        job_id=job.id,
                        skill_id=skill['id']
                    )
                    db.session.add(skill_job)
                db.session.commit()

            del data['skills']
            data['id'] = job.id
            analyzer.store_job(**data)

            return "job added. job={}".format(job.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400


class HandleJob(Resource):
    """
    This class is used to get job data using job ID or update job data or delete job
    """

    # method_decorators = {'put': [only_recruiter_creator_of_job], 'get': [only_authenticated],
    #                      'delete': [only_recruiter_creator_of_job]}

    def get(self, job_id):
        """
        Get user
        """
        try:
            job_object = Job.query.filter_by(id=job_id).first()
            serialized_job = job_object.serialize()
            return jsonify(serialized_job)
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
                UserApplication.query.filter_by(job_id=job_id).delete()
                UserJobRecommendation.query.filter_by(job_id=job_id).delete()
                job_object.delete()
                db.session.commit()

                analyzer.delete_job(job_id)

                return "Job with ID: {} deleted".format(job_id)
            else:
                return "Job does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class UserJobApplication(Resource):
    """This class is used to create a user-application for a job """

    # method_decorators = {'post': [only_lifelong_learner], 'delete': [only_profile_owner]}

    def post(self, user_id, job_id):
        """
        Create user-job relationship
        """
        data = request.get_json()

        try:
            user_job = UserApplication(
                user_id=user_id,
                job_id=job_id,
                available=data['available'],
                exp_salary=data['expsalary']
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
            UserApplication.query.filter_by(user_id=user_id, job_id=job_id).delete()
            db.session.commit()
            return "job application for job with ID: {} and user with ID: {} deleted".format(job_id, user_id)
        except Exception as ex:
            log.error(ex)
            return ex


class JobApplication(Resource):
    """This class is used to retrieve all applicants for a job """

    # method_decorators = {'get': [only_recruiter_creator_of_job]}

    def get(self, job_id):
        """
        retrieve all applicants
        """
        try:
            print(job_id)
            applicants = UserApplication.query.filter_by(job_id=job_id)
            serialized_applicants = [applicant.serialize() for applicant in applicants]
            return jsonify(applicants=serialized_applicants)
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfApplicationsByUser(Resource):
    """Get user's job applications"""

    # method_decorators = {'get': [only_profile_owner]}

    def get(self, user_id):
        try:
            user_applications = UserApplication.query.filter_by(user_id=user_id)
            serialized_applications = [user_application.serialize() for user_application in user_applications]
            return jsonify(jobs=serialized_applications)
        except Exception as ex:
            log.error(ex)
            return ex


class SkillsToJob(Resource):
    """This interface appends skills to courses"""

    # method_decorators = {'post': [only_recruiter_creator_of_job], 'get': [only_authenticated]}

    def post(self, job_id):
        try:
            data = request.get_json()

            job_id = job_id
            skill_id = data['skill_id']

            if_relation_exists = JobSkill.query.filter_by(job_id=job_id, skill_id=skill_id).scalar()
            if if_relation_exists:
                return {'msg': "relation already exists"}, 400
            else:
                skill_job = JobSkill(
                    job_id=job_id,
                    skill_id=skill_id
                )
                db.session.add(skill_job)
                db.session.commit()

                skill_object = Skill.query.filter_by(id=skill_id).first()
                serialized_object = skill_object.serialize()

                analyzer.add_skill(
                    job_id=job_id,
                    new_skill=serialized_object["name"]
                )

        except Exception as ex:
            log.error(ex)
            return ex

    def get(self, job_id):
        try:
            job_skills = JobSkill.query.filter_by(
                job_id=job_id
            )
            results = [{
                "id": job_skill.skill.__dict__['id'],
                'name': job_skill.skill.__dict__['name'],
                "type": job_skill.skill.__dict__['type'],
                "hard_skill": job_skill.skill.__dict__['hard_skill']
            } for job_skill in job_skills]
            return results, 200
        except Exception as ex:
            log.error(ex)
            return ex


class SelectLocation(Resource):

    # method_decorators = {'get': [only_authenticated]}

    def get(self):
        try:
            args = request.args
            universal_api = CitiesClient()

            country = args.get('country', None)
            state = args.get('state', None)

            if country:
                response = universal_api.get_country_states(country)
                api_result = response.json()
                return api_result
            if state:
                response = universal_api.get_state_cities(state)
                api_result = response.json()
                return api_result
            if state is None and country is None:
                response = universal_api.get_countries()
                api_result = response.json()
                return api_result

        except Exception as ex:
            log.error(ex)
            return ex


class SearchForJob(Resource):
    # method_decorators = {'get': [only_authenticated]}

    def get(self):
        try:
            args = dict(request.args)

            search_results = analyzer.search_job(**args)
            response_status_code = search_results.status_code

            if response_status_code != 201:
                log.error(response_status_code.reason)
                return {'msg': "Bad request"}, 400
            else:
                json_results = search_results.json()
            return json_results, 200
        except Exception as ex:
            log.error(ex)
            return ex


class SpecializationObject(Resource):
    def get(self):
        """
        Get All Specializations
        """

        try:
            specializations = Specialization.query.all()
            serialized_specs = [specialization.serialize() for specialization in specializations]
            return jsonify(serialized_specs)

        except Exception as ex:
            log.error(ex)

    def post(self):
        """
        Add a specialization
        """
        data = dict(request.get_json())

        try:
            specialization = Specialization(
                title=data['title'],
            )
            db.session.add(specialization)
            db.session.commit()

            return "specialization added. specialization={}".format(specialization.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def delete(self):
        """
        delete a specialization
        """
        data = dict(request.get_json())
        try:
            Specialization.query.filter_by(id=data['id']).delete()
            db.session.commit()
            return "specialization with ID: {} deleted".format(data['id'])
        except Exception as ex:
            log.error(ex)
            return ex

# Job Routes


api.add_resource(JobObject, '/jobs')
api.add_resource(HandleJob, '/jobs/<job_id>')
api.add_resource(SkillsToJob, '/jobs/<job_id>/skills')

api.add_resource(UserJobApplication, '/jobs/<job_id>/apply/<user_id>')
api.add_resource(JobApplication, '/jobs/<job_id>/apply/')
api.add_resource(GetListOfApplicationsByUser, '/users/<user_id>/jobapplies')
api.add_resource(SelectLocation, '/select/location')
api.add_resource(SearchForJob, '/job/search')

api.add_resource(SpecializationObject, '/specializations')
