# =================================
#   Course APIs
# =================================
import logging
import sys
from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource, Api

from application.courses import course_blueprint
from application.database import db
from application.models import UserCourse, Skill, UserCourseRecommendation, BadgeCourseRelation, \
    UserSkillRecommendation, Course, SkillCourse, AcademicOrganisation

from application.utils import assign_grade, kpi_measurement
from application.decorators import only_professors_or_academic_oranisations, \
    only_professor_or_academic_organisation_of_course, only_profile_owner, only_lifelong_learner, only_authenticated, \
    only_profile_owner_or_professor_or_academic_organisation_of_course

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(course_blueprint)


class CourseObject(Resource):
    """
    This object is used to:

    1) Create a new Course
    2) Get all stored courses
    """

    method_decorators = {'post': [only_professors_or_academic_oranisations], 'get': [only_authenticated]}

    def post(self):
        """
        Append new Course
        """
        data = request.get_json()

        try:
            course = Course(
                name=data['name'],
                description=data['description'],
                semester=data['semester'],
                updatedDate=data['updatedDate'] if 'updatedDate' in data.keys() else datetime.now().strftime(
                    "%b %d %Y, %H:%M:%S"),
                events=data['events'],
                academic_organisation_id=data['academic_organisation_id'],
                start_date=data['start_date'],
                end_date=data['end_date']
            )

            db.session.add(course)
            db.session.commit()
            skills_in_data = 'skills' in data.keys()
            if skills_in_data:
                for skill in data['skills']:
                    new_skill = SkillCourse(skill_id=skill['id'], course_id=course.id)
                    db.session.add(new_skill)
                db.session.commit()
            kpi_measurement('create_course')
            return "Course added. course={}".format(course.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """
        Get All Courses
        """
        try:
            courses = Course.query.all()
            serialized_courses = [course.serialize() for course in courses]
            return jsonify(serialized_courses)

        except Exception as ex:
            log.error(ex)


class SkillsToCourses(Resource):
    """This interface appends skills to courses"""

    method_decorators = {'post': [only_professor_or_academic_organisation_of_course],
                         'get': [only_authenticated]}

    def post(self, course_id):
        try:
            data = request.get_json()
            skill_id = data['skill_id']

            skill_course = SkillCourse(
                course_id=course_id,
                skill_id=skill_id
            )
            db.session.add(skill_course)
            db.session.commit()
        except Exception as ex:
            log.error(ex)
            return ex

    def get(self, course_id):
        """
        Get all skills from the given course
        """
        try:
            course_skills = SkillCourse.query.filter_by(
                course_id=course_id
            )
            results = [skill_course_rel.serialize_skillsofacourse() for skill_course_rel in course_skills]
            return results, 200
        except Exception as ex:
            log.error(ex)
            return ex


class HandleCourse(Resource):
    """This class is used to get/put a specified course"""

    method_decorators = {'get':[only_authenticated], 'put': [only_professor_or_academic_organisation_of_course],
                         'delete': [only_professor_or_academic_organisation_of_course]}

    def get(self, course_id):
        """
        Get specific Course
        """
        try:
            course_object = Course.query.filter_by(id=course_id).first()
            serialized_course = course_object.serialize()
            return jsonify(serialized_course)
        except Exception as ex:
            log.error(ex)
            return ex

    def put(self, course_id):
        """
        Update course data
        """
        data = dict(request.get_json())

        try:
            course_object = Course.query.filter_by(id=course_id)
            skills_in_data = 'skills' in data.keys()
            if skills_in_data:
                SkillCourse.query.filter_by(course_id=course_id).delete()
                skills = data['skills']
                del data['skills']
                for skill in skills:
                    skill_id = skill['id']
                    new_skill_course = SkillCourse(skill_id=skill_id, course_id=course_object[0].id)
                    db.session.add(new_skill_course)
                    db.session.commit()

            if len(data) != 0:
                course_object.update(data)
                db.session.commit()
            if course_object[0].academic_organisation_id is None:
                kpi_measurement('update_course')
            else:
                kpi_measurement('update_' + AcademicOrganisation.query.filter_by(
                    id=course_object[0].academic_organisation_id).first().title + '_course')
            return "course with ID: {} updated".format(course_id)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, course_id):
        """ delete course """
        try:
            course_object = Course.query.filter_by(id=course_id)
            if course_object.first():
                UserCourse.query.filter_by(course_id=course_id).delete()
                UserCourseRecommendation.query.filter_by(course_id=course_id).delete()
                BadgeCourseRelation.query.filter_by(course_id=course_id).delete()
                SkillCourse.query.filter_by(course_id=course_id).delete()
                # skills = Skill.query.filter_by(course_id=course_id).all()
                # for skill in skills:
                #     UserSkillRecommendation.query.filter_by(skill_id=skill.id).delete()
                # Skill.query.filter_by(course_id=course_id).delete()
                course_object.delete()
                db.session.commit()
                return "Course with ID: {} deleted".format(course_id)
            else:
                return "Course does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfUsersOfCourse(Resource):
    """Get list of users of a specific course"""

    method_decorators = {'get': [only_professor_or_academic_organisation_of_course]}

    def get(self, course_id):
        try:
            user_courses = UserCourse.query.filter_by(course_id=course_id)
            serialized_users = [user_course_rel.serialize_usersofacourse() for user_course_rel in user_courses]
            return serialized_users, 200
        except Exception as ex:
            log.error(ex)
            return ex

    def post(self, course_id):
        try:
            data = dict(request.get_json())
            if 'course_status' in data.keys():
                user_courses = UserCourse.query.filter_by(course_id=course_id, course_status=data['course_status'])
            else:
                user_courses = UserCourse.query.filter_by(course_id=course_id)
            serialized_users = [user_course_rel.serialize_usersofacourse() for user_course_rel in user_courses]
            return serialized_users, 200
        except Exception as ex:
            log.error(ex)
            return ex


class CheckUserCourseRelation(Resource):
    """This interface investigates user-course relation"""

    method_decorators = {'get': [only_profile_owner_or_professor_or_academic_organisation_of_course]}

    def get(self, course_id, user_id, status):
        try:
            user_courses_relation = UserCourse.query.filter_by(
                course_id=course_id,
                user_id=user_id,
                course_status=status)
            if user_courses_relation.scalar():
                return {'exists': True}, 200
            else:
                return {'exists': False}, 200
        except Exception as ex:
            log.error(ex)
            return ex


class CreateUserCourseRelation(Resource):
    """This class is used to create a user-course relationship"""
    method_decorators = {'post': [only_profile_owner_or_professor_or_academic_organisation_of_course]}

    def post(self, user_id):
        """
        Create user-course relationship
        """
        data = dict(request.get_json())

        grade = data['grade'] if "grade" in data.keys() else None
        final_grade = assign_grade(data['course_status'], grade)
        courses_status = data['course_status']

        user_course = UserCourse.query.filter_by(
            course_id=data['course_id'],
            user_id=user_id
        )
        try:
            if user_course.scalar():
                user_course.update(data)
            else:
                user_course = UserCourse(
                    user_id=user_id,
                    course_id=data['course_id'],
                    course_status=courses_status,
                    grade=final_grade

                )
                db.session.add(user_course)
            db.session.commit()
            return "relationship for user={} and course={} created".format(user_id, data['course_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex



class HandleUserCourseRelation(Resource):
    """This class is used to delete a user-course relationship"""

    method_decorators = {'delete': [only_profile_owner]}

    def delete(self, user_id, course_id):
        """
        Delete user-course relationship
        """
        try:
            user_course = UserCourse.query.filter_by(user_id=user_id, course_id=course_id)
            if user_course.first():
                user_course.delete()
                db.session.commit()
                return "Relation between course with ID={} and user with ID={} removed".format(course_id, user_id)
            else:
                return "Relation between course with ID={} and user with ID={} does not exist".format(course_id,
                                                                                                      user_id), 404
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfCoursesTeached(Resource):
    """Get list of courses teached by a specific user"""

    method_decorators = {'get': [only_authenticated]}

    def get(self, user_id):
        try:
            user_courses = UserCourse.query.filter_by(user_id=user_id, course_status="taught")
            serialized_courses = [user_course_rel.serialize() for user_course_rel in user_courses]
            return serialized_courses, 200
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfTeachersOfCourse(Resource):
    """Get list of teachers teaching a course"""

    def get(self, course_id, status):
        try:
            user_courses = UserCourse.query.filter_by(course_id=course_id, course_status="taught")
            serialized_courses = [user_course_rel.serialize() for user_course_rel in user_courses]
            return serialized_courses, 200
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfCoursesCompletedByLearner(Resource):
    """Get list of courses completed by a specific user"""

    method_decorators = {'get': [only_profile_owner]}

    def get(self, user_id):
        try:
            user_courses = UserCourse.query.filter(UserCourse.user_id == user_id,
                                                   UserCourse.course_status.in_(("done", "assisted")))
            serialized_courses = [user_course_rel.serialize() for user_course_rel in user_courses]
            return serialized_courses, 200
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfCoursesByOrganisation(Resource):
    """Get list of courses related to an academic organisation"""

    def get(self, academic_organisation_id):
        try:
            courses = Course.query.filter_by(academic_organisation_id=academic_organisation_id)
            serialized_courses = [course.serialize() for course in courses]
            return serialized_courses, 200
        except Exception as ex:
            log.error(ex)
            return ex


# Course Routes
api.add_resource(CourseObject, '/courses')
api.add_resource(HandleCourse, '/courses/<course_id>')
api.add_resource(GetListOfUsersOfCourse, '/courses/<course_id>/users')
api.add_resource(SkillsToCourses, '/courses/<course_id>/skills')
api.add_resource(GetListOfCoursesByOrganisation, '/courses/academicorganisation/<academic_organisation_id>')

api.add_resource(CreateUserCourseRelation, '/users/<user_id>/courses')
api.add_resource(HandleUserCourseRelation, '/users/<user_id>/courses/<course_id>')
api.add_resource(GetListOfCoursesTeached, '/courses/teachingcourses/<user_id>')
api.add_resource(GetListOfCoursesCompletedByLearner, '/courses/completedcourses/<user_id>')
api.add_resource(CheckUserCourseRelation, '/courses/<course_id>/users/<user_id>/status/<status>')
api.add_resource(GetListOfTeachersOfCourse, '/courses/<course_id>/status/<status>')
