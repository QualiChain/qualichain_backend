import logging
import sys

from flask import request
from flask_restful import Resource, Api

from application.database import db
from application.models import UserCourseRecommendation, UserSkillRecommendation, UserJobRecommendation
from application.recommendations import recommendation_blueprint
from application.decorators import only_profile_owner

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(recommendation_blueprint)


class CoursesRecommendation(Resource):
    """This class is used to create a user-course recommendation"""

    method_decorators = {'get': [only_profile_owner]}

    def post(self, user_id):
        """
        Create user-course recommendation
        """
        data = request.get_json()

        try:
            recommendation = UserCourseRecommendation(
                user_id=user_id,
                course_id=data['course_id'],
                rating=data['rating']
            )
            db.session.add(recommendation)
            db.session.commit()
            return "recommendation for user={} and course={} created".format(user_id, data['course_id']), 201

        except Exception as ex:
            log.error(ex)
            return ex

    def get(self, user_id):
        try:
            rec_courses = UserCourseRecommendation.query.filter_by(user_id=user_id)
            serialized_courses = [crs.serialize() for crs in rec_courses]
            return serialized_courses, 200
        except Exception as ex:
            log.error(ex)
            return ex


class HandleUserCourseRecommendation(Resource):
    """
    This class is used to handle a specific user-course relation
    """

    def delete(self, user_id, course_id):
        """ delete a specific user - course recommendation """
        try:
            recommendation = UserCourseRecommendation.query.filter_by(user_id=user_id, course_id=course_id)
            if recommendation.first():
                recommendation.delete()
                db.session.commit()
                return "Recommendation of course with ID={} for user with ID={} removed".format(course_id, user_id)
            else:
                return "Recommendation of course with ID={} for user with ID={} does not exist".format(course_id,
                                                                                                       user_id), 404
        except Exception as ex:
            log.error(ex)
            return ex, 404


class SkillsRecommendation(Resource):
    """This class is used to create a user-skill recommendation"""

    method_decorators = {'get': [only_profile_owner]}

    def post(self, user_id):
        """
        Create user-skill recommendation
        """
        data = request.get_json()

        try:
            recommendation = UserSkillRecommendation(
                user_id=user_id,
                skill_id=data['skillId'],
                description=data['description'],
                related_jobs=data['relatedJobs'],
                relevant_skills=data['relevantSkills']
            )
            db.session.add(recommendation)
            db.session.commit()
            return "recommendation for user={} and skill={} created".format(user_id, data['skillId']), 201

        except Exception as ex:
            log.error(ex)
            return ex

    def get(self, user_id):
        try:
            rec_skills = UserSkillRecommendation.query.filter_by(user_id=user_id)
            serialized_skills = [skl.serialize() for skl in rec_skills]
            return serialized_skills, 200
        except Exception as ex:
            log.error(ex)
            return ex


class HandleUserSkillRecommendation(Resource):
    """
    This class is used to handle a specific user-skill relation
    """

    def delete(self, user_id, skill_id):
        """ delete a specific user - skill recommendation """
        try:
            recommendation = UserSkillRecommendation.query.filter_by(user_id=user_id, skill_id=skill_id)
            if recommendation.first():
                recommendation.delete()
                db.session.commit()
                return "Recommendation of skill with ID={} for user with ID={} removed".format(skill_id, user_id)
            else:
                return "Recommendation of skill with ID={} for user with ID={} does not exist".format(skill_id,
                                                                                                      user_id), 404
        except Exception as ex:
            log.error(ex)
            return ex, 404


class JobsRecommendation(Resource):
    """This class is used to create a user-job recommendation"""

    method_decorators = {'get': [only_profile_owner]}

    def post(self, user_id):
        """
        Create user-job recommendation
        """
        data = request.get_json()

        try:
            recommendation = UserJobRecommendation(
                user_id=user_id,
                job_id=data['jobId']
            )
            db.session.add(recommendation)
            db.session.commit()
            return "recommendation for user={} and job={} created".format(user_id, data['jobId']), 201

        except Exception as ex:
            log.error(ex)
            return ex

    def get(self, user_id):
        try:
            rec_jobs = UserJobRecommendation.query.filter_by(user_id=user_id)
            serialized_jobs = [job.serialize() for job in rec_jobs]
            return serialized_jobs, 200
        except Exception as ex:
            log.error(ex)
            return ex


class HandleUserJobRecommendation(Resource):
    """
    This class is used to handle a specific user-job relation
    """

    def delete(self, user_id, job_id):
        """ delete a specific user - job recommendation """
        try:
            recommendation = UserJobRecommendation.query.filter_by(user_id=user_id, job_id=job_id)
            if recommendation.first():
                recommendation.delete()
                db.session.commit()
                return "Recommendation of job with ID={} for user with ID={} removed".format(job_id, user_id)
            else:
                return "Recommendation of job with ID={} for user with ID={} does not exist".format(job_id,
                                                                                                    user_id), 404
        except Exception as ex:
            log.error(ex)
            return ex, 404


# Recommendations routes
api.add_resource(SkillsRecommendation, '/recommendations/<user_id>/skills')
api.add_resource(HandleUserSkillRecommendation, '/recommendations/<user_id>/skills/<skill_id>')
api.add_resource(CoursesRecommendation, '/recommendations/<user_id>/courses')
api.add_resource(HandleUserCourseRecommendation, '/recommendations/<user_id>/courses/<course_id>')
api.add_resource(JobsRecommendation, '/recommendations/<user_id>/jobs')
api.add_resource(HandleUserJobRecommendation, '/recommendations/<user_id>/jobs/<job_id>')
