import logging
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

import producer
from clients.fuseki_client import FusekiClient
from settings import APP_SETTINGS

'''Run flask by executing the command python -m flask run'''

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

app.config.from_object(APP_SETTINGS)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)

from models import Book, User, Skill, Job, UserJob, Course, UserCourse, CV, Notification, UserCourseRecommendation, \
    UserSkillRecommendation, UserJobRecommendation, SmartBadge, BadgeCourseRelation, UserBadgeRelation


@app.route('/retrieve_data', methods=['POST'])
def retrieve_saro_data():
    '''
    This api call executes a query and retrieves data from a knowledge graph.
    Post body(json):
    {"query": "String SparQL query to be executed"}
    :return: Returns the results of the query in JSON format.
    '''

    request_data = request.get_json()
    if request_data is not None:
        query = request_data['query']
        fuseki_client = FusekiClient()
        response = fuseki_client.query_fuseki_client(query)
        if response.status_code == 200:
            description = 'Query Completed'
            results = response.json()
            status = response.status_code
        else:
            description = 'Incorrect Query'
            results = {}
            status = response.status_code
    else:
        description = 'Incorrect Request'
        results = {}
        status = '500'

    results = {'status': status, 'results': results, 'description': description}

    return jsonify(results)


@app.route('/submit_data', methods=['POST'])
def submit_saro_data():
    '''
    This api call submits data to Dobie in order to store the result in the knowledge graph.
    Post body(json):
    {"text": "The text that will be analysed in Dobie}
    '''

    request_data = request.get_json()
    if request_data is not None:
        text = request_data['text']
        producer.add_to_queue(text)
        description = 'Submission Completed'
    else:
        description = 'Incorrect Request'
    results = {'description': description}
    return jsonify(results)


# =================================
#   User APIs
# =================================

class UserObject(Resource):
    """
    This class is used to create a new User or to get All stored users
    """

    def post(self):
        """
        Create a new User
        """
        data = request.get_json()

        try:
            user = User(
                userPath=data['userPath'],
                role=data['role'],
                pilotId=data['pilotId'],
                userName=data['userName'],
                fullName=data['fullName'],
                name=data['name'],
                surname=data['surname'],
                gender=data['gender'],
                birthDate=data['birthDate'],
                country=data['country'],
                city=data['city'],
                address=data['address'],
                zipCode=data['zipCode'],
                mobilePhone=data['mobilePhone'],
                homePhone=data['homePhone'],
                email=data['email']
            )
            db.session.add(user)
            db.session.commit()
            return "user added. user={}".format(user.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """
        Get All Users
        """
        try:
            users = User.query.all()
            serialized_users = [usr.serialize() for usr in users]
            return jsonify(serialized_users)

        except Exception as ex:
            log.error(ex)


class HandleUser(Resource):
    """
    This class is used to get user using his ID or update user data
    """

    def get(self, user_id):
        """
        Get user
        """
        try:
            user_object = User.query.filter_by(id=user_id).first()
            serialized_user = user_object.serialize()
            return serialized_user
        except Exception as ex:
            log.info(ex)
            return "user with ID: {} does not exist".format(user_id), 404

    def put(self, user_id):
        """
        Update user data
        """
        data = dict(request.get_json())

        try:
            user_object = User.query.filter_by(id=user_id)
            user_object.update(data)
            db.session.commit()
            return "user with ID: {} updated".format(user_id)
        except Exception as ex:
            log.error(ex)
            return ex


class NewPassword(Resource):
    """This class is used to set user's password"""

    def post(self, user_id):
        """
        This function is used to set user password using POST request
        """
        data = request.get_json()

        try:
            user_object = User.query.filter_by(id=user_id).first()

            user_pwd = data['password']
            user_object.set_password(user_pwd)
            db.session.commit()
            return "User's {} password created successfully".format(user_id)
        except Exception as ex:
            log.error(ex)
            return ex


class ChangePassword(Resource):
    """This class updates user's password"""

    def post(self, user_id):
        data = dict(request.get_json())

        try:
            user_object = User.query.filter_by(id=user_id).first()

            new_pwd = data["new_password"]
            user_object.set_password(new_pwd)
            db.session.commit()
            return "User's {} password updated successfully".format(user_id)
        except Exception as ex:
            log.error(ex)
            return ex


# =================================
#   Auth APIs
# =================================

class Authentication(Resource):
    """
    This class is used to authenticate Qualichain users
    """

    def post(self):
        """Authentication using password and username"""
        try:
            data = request.get_json()

            username = data['username']
            pwd = data['password']

            user_obj = User.query.filter_by(userName=username).first()
            is_registered_user = user_obj.check_password(pwd)

            if is_registered_user:
                serialized_user = user_obj.serialize()
                return jsonify(serialized_user)
            else:
                return "User doesn't exist or password is wrong", 404
        except Exception as ex:
            log.error(ex)
            return "User doesn't exist or password is wrong", 404


# =================================
#   Skill APIs
# =================================
class SkillObject(Resource):
    """This object is used to create new skills and return all stored skills"""

    def post(self):
        """Create new skill"""
        data = request.get_json()

        try:
            skill = Skill(
                name=data['name'],
                course_id=data['course_id'] if 'course_id' in data.keys() else None
            )
            db.session.add(skill)
            db.session.commit()
            return "skill with ID: {} added".format(skill.id), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get all skills"""
        try:
            skill_objs = Skill.query.all()
            serialized_skills = [skill.serialize() for skill in skill_objs]
            return jsonify(serialized_skills)
        except Exception as ex:
            log.error(ex)
            return ex


class HandleSkill(Resource):
    """Class to handle skills"""

    def get(self, skill_id):
        """Get specific skill"""
        try:
            skill_obj = Skill.query.filter_by(id=skill_id).first()
            serialized_skill = skill_obj.serialize()
            return serialized_skill, 200
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self, skill_id):
        """ delete skill """
        try:
            skill_obj = Skill.query.filter_by(id=skill_id)
            if skill_obj.first():
                UserSkillRecommendation.query.filter_by(skill_id=skill_id).delete()
                skill_obj.delete()
                db.session.commit()
                return "Skill with ID: {} deleted".format(skill_id)
            else:
                return "Skill does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


# =================================
#   Job APIs
# =================================

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
    This class is used to get job data using job ID or update job data
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


# =================================
#   Course APIs
# =================================

class CourseObject(Resource):
    """
    This object is used to:

    1) Create a new Course
    2) Get all stored courses
    """

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
                endDate=data['endDate'],
                startDate=data['startDate'],
                updatedDate=data['updatedDate'],
                events=data['events']
            )

            db.session.add(course)
            db.session.commit()
            for skill in data['skills']:
                new_skill = Skill(
                    name=skill['name'],
                    course_id=course.id
                )
                db.session.add(new_skill)
                db.session.commit()
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


class HandleCourse(Resource):
    """This class is used to get/put a specified course"""

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
            skills_in_data = 'skills' in data
            if skills_in_data == True:
                skills = data['skills']
                del data['skills']
                for skill in skills:
                    skill_object = Skill.query.filter_by(name=skill['name'], course_id=course_id).all()
                    if len(skill_object) == 0:
                        new_skill = Skill(
                            name=skill['name'],
                            course_id=course_id
                            )
                        db.session.add(new_skill)
                        db.session.commit()
            if len(data) != 0:
                course_object.update(data)
                db.session.commit()
            return "course with ID: {} updated".format(course_id)
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfUsersOfCourse(Resource):
    """Get list of users of a specific course"""

    def get(self, course_id):
        try:
            user_courses = UserCourse.query.filter_by(course_id=course_id, course_status="enrolled")
            serialized_users = [user_course_rel.serialize_usersofacourse() for user_course_rel in user_courses]
            return serialized_users, 200
        except Exception as ex:
            log.error(ex)
            return ex


class CreateUserCourseRelation(Resource):
    """This class is used to create a user-course relationship"""

    def post(self, user_id):
        """
        Create user-course relationship
        """
        data = request.get_json()

        try:
            user_course = UserCourse(
                user_id=user_id,
                course_id=data['course_id'],
                course_status=data['course_status']
            )
            db.session.add(user_course)
            db.session.commit()
            return "relationship for user={} and course={} created".format(user_id, data['course_id']), 201

        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfCoursesTeached(Resource):
    """Get list of courses teached by a specific user"""

    def get(self, user_id):
        try:
            user_courses = UserCourse.query.filter_by(user_id=user_id, course_status="teached")
            serialized_courses = [user_course_rel.serialize() for user_course_rel in user_courses]
            return serialized_courses, 200
        except Exception as ex:
            log.error(ex)
            return ex


class GetListOfCoursesCompletedByLearner(Resource):
    """Get list of courses completed by a specific user"""

    def get(self, user_id):
        try:
            user_courses = UserCourse.query.filter_by(user_id=user_id, course_status="done")
            serialized_courses = [user_course_rel.serialize() for user_course_rel in user_courses]
            return serialized_courses, 200
        except Exception as ex:
            log.error(ex)
            return ex


class HandleCV(Resource):
    """
    This class is used to create a new CV for user or retrieve the CV of a user
    """

    def post(self, user_id):
        """
        Create a new User
        """
        data = request.get_json()

        try:
            cv = CV(
                user_id=user_id,
                person_URI=data['PersonURI'],
                label=data['Label'],
                target_sector=data['targetSector'],
                expected_salary=data['expectedSalary'],
                description=data['Description'],
                skills=data['Skills'],
                work_history=data['workHistory'],
                education=data['Education']
            )
            db.session.add(cv)
            db.session.commit()
            return "CV added for user={}".format(user_id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self, user_id):
        """
        Get the CV of a user
        """
        try:
            cvs = CV.query.filter_by(user_id=user_id)
            serialized_cvs = [cv.serialize() for cv in cvs]
            return jsonify(serialized_cvs)

        except Exception as ex:
            log.error(ex)


# =================================
#   Notification APIs
# =================================
class NotificationObject(Resource):
    def post(self):
        data = request.get_json()

        try:
            notification_obj = Notification(
                message=data['message'],
                user_id=data['user_id']
            )

            db.session.add(notification_obj)
            db.session.commit()
            return 'Notification added for UserID={}'.format(data['user_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        user_id = request.args.get('userid', None)

        try:
            if user_id:
                notifications = Notification.query.filter_by(user_id=user_id)
            else:
                notifications = Notification.query.all()

            serialized_notifications = [notification.serialize() for notification in notifications]
            return serialized_notifications, 200
        except Exception as ex:
            log.error(ex)
            return ex, 404


class HandleNotification(Resource):
    def get(self, notification_id):
        try:
            notification = Notification.query.filter_by(id=notification_id).first()
            serialized_notification = notification.serialize()
            return serialized_notification, 200
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def post(self, notification_id):
        try:
            notification = Notification.query.filter_by(id=notification_id).first()

            if notification.readed:
                notification.readed = False
                message = "Notification with ID={} Read status={}".format(notification_id, 'False')
            else:
                notification.readed = True
                message = "Notification with ID={} Read status={}".format(notification_id, 'True')

            db.session.commit()
            return message, 201
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self, notification_id):
        try:
            notification = Notification.query.filter_by(id=notification_id)
            notification.delete()
            db.session.commit()
            return "Notification with ID={} removed".format(notification_id), 204
        except Exception as ex:
            log.error(ex)
            return ex, 404


class CoursesRecommendation(Resource):
    """This class is used to create a user-course recommendation"""

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


class SkillsRecommendation(Resource):
    """This class is used to create a user-skill recommendation"""

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


class JobsRecommendation(Resource):
    """This class is used to create a user-job recommendation"""

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


# =================================
#   SmartBadge APIs
# =================================
class SmartBadgeObject(Resource):
    """This class is used to Create a new Smart Badge and retrieve all stored Smart Badges"""

    def post(self):
        """Create a new Smart Badge"""
        data = request.get_json()

        try:
            smart_badge = SmartBadge(
                name=data['name'],
                issuer=data['issuer'],
                description=data['description']
            )
            db.session.add(smart_badge)
            db.session.commit()
            return "smart badge with ID={} created".format(smart_badge.id), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get all stored smart badges"""
        try:
            smart_badges = SmartBadge.query.all()
            serialized_badges = [badge.serialize() for badge in smart_badges]
            return serialized_badges, 200
        except Exception as ex:
            log.error(ex)
            return ex


class HandleSmartBadge(Resource):
    """This object is used to handle a specific smart badge"""

    def get(self, badge_id):
        try:
            smart_badge = SmartBadge.query.filter_by(id=badge_id).first()
            serialized_badge = smart_badge.serialize()
            return serialized_badge, 200
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self, badge_id):
        """ delete a specific smart badge """
        try:
            smart_badge = SmartBadge.query.filter_by(id=badge_id)
            if smart_badge.first():
                UserBadgeRelation.query.filter_by(badge_id=badge_id).delete()
                BadgeCourseRelation.query.filter_by(badge_id=badge_id).delete()
                smart_badge.delete()
                db.session.commit()
                return "Smart badge with ID={} deleted".format(badge_id)
            else:
                return "Smart badge with ID={} does not exist".format(badge_id), 404
        except Exception as ex:
            log.error(ex)
            return ex, 404


class CourseBadgeAssignment(Resource):
    """This class is used to handle Course - Badge Relation"""

    def post(self):
        """Create Course - Badge Relation"""
        data = request.get_json()

        try:
            relation = BadgeCourseRelation(
                course_id=data['course_id'],
                badge_id=data['badge_id']
            )

            db.session.add(relation)
            db.session.commit()
            return "relation between CourseID={} and BadgeID={} created".format(data['course_id'],
                                                                                data['badge_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get Course - Badge Relation"""
        course_id = request.args.get('courseid', None)

        try:
            if course_id:

                course_badges = BadgeCourseRelation.query.filter_by(course_id=course_id)
            else:
                course_badges = BadgeCourseRelation.query.all()

            serialized_relations = [relation.serialize() for relation in course_badges]
            return serialized_relations, 200

        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self):
        """Delete Course - Badge Relation"""
        course_id = request.args.get('courseid', None)
        badge_id = request.args.get('badgeid', None)

        if course_id and badge_id:
            try:
                course_badges = BadgeCourseRelation.query.filter_by(course_id=course_id, badge_id=badge_id)

                if course_badges:
                    course_badges.delete()
                    db.session.commit()
                else:
                    return "Course - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "Bad Request", 400


class UserBadgeAssignment(Resource):
    """This class is used to handle User - Badge Relation"""

    def post(self):
        """Create User - Badge Relation"""
        data = request.get_json()

        try:
            relation = UserBadgeRelation(
                badge_id=data['badge_id'],
                user_id=data['user_id']
            )

            db.session.add(relation)
            db.session.commit()
            return "relation between UserID={} and BadgeID={} created".format(data['user_id'], data['badge_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get User - Badge Relation"""
        user_id = request.args.get('userid', None)

        try:
            if user_id:

                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id)
            else:
                user_badges = UserBadgeRelation.query.all()

            serialized_relations = [relation.serialize() for relation in user_badges]
            return serialized_relations, 200

        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self):
        """Delete User - Badge Relation"""

        user_id = request.args.get('userid', None)
        badge_id = request.args.get('badgeid', None)

        if user_id and badge_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id)
                print(user_badges)

                if user_badges:
                    user_badges.delete()
                    db.session.commit()
                else:
                    return "User - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "Bad Request", 400


# =================================
#   Mediator API Routes
# =================================

# User Routes
api.add_resource(UserObject, '/users')
api.add_resource(HandleUser, '/users/<user_id>')

api.add_resource(NewPassword, '/users/<user_id>/requestnewpassword')
api.add_resource(ChangePassword, '/users/<user_id>/updatePassword')

# Auth Routes
api.add_resource(Authentication, '/auth')

# Skill Routes
api.add_resource(SkillObject, '/skills')
api.add_resource(HandleSkill, '/skills/<skill_id>')

# Job Routes
api.add_resource(JobObject, '/jobs')
api.add_resource(HandleJob, '/jobs/<job_id>')

api.add_resource(UserJobApplication, '/jobs/<job_id>/apply/<user_id>')
api.add_resource(JobApplication, '/jobs/<job_id>/apply/')
api.add_resource(GetListOfApplicationsByUser, '/users/<user_id>/jobapplies')

# Course Routes
api.add_resource(CourseObject, '/courses')
api.add_resource(HandleCourse, '/courses/<course_id>')
api.add_resource(GetListOfUsersOfCourse, '/courses/<course_id>/users')

api.add_resource(CreateUserCourseRelation, '/users/<user_id>/courses')
api.add_resource(GetListOfCoursesTeached, '/courses/teachingcourses/<user_id>')
api.add_resource(GetListOfCoursesCompletedByLearner, '/courses/completedcourses/<user_id>')

# CVs routes
api.add_resource(HandleCV, '/CV/<user_id>')

# Notification Routes
api.add_resource(NotificationObject, '/notifications')
api.add_resource(HandleNotification, '/notifications/<notification_id>')

# Recommendations routes
api.add_resource(SkillsRecommendation, '/recommendations/<user_id>/skills')
api.add_resource(CoursesRecommendation, '/recommendations/<user_id>/courses')
api.add_resource(JobsRecommendation, '/recommendations/<user_id>/jobs')

# Smart Badges Routes
api.add_resource(SmartBadgeObject, '/badges')
api.add_resource(HandleSmartBadge, '/badges/<badge_id>')

api.add_resource(CourseBadgeAssignment, '/course/badges')

api.add_resource(UserBadgeAssignment, '/user/badges')
