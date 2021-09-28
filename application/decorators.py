from functools import wraps

import flask_restful
from flask import request

from application.models import Notification, UserCourse, Job
from application.utils import get_authenticated_user, check_if_profile_owner, get_user_id_from_request, \
    get_user_id_from_cv_id_of_request, get_jobs_of_recruiter, has_applied_for_jobs, get_courses_of_professor, \
    attends_course


def only_profile_owner(func):
    """Decorator that is used for user authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id, mock_user_obj, mock_user_roles = check_if_profile_owner(*args, **kwargs)
        print(user_id, mock_user_obj, mock_user_roles)

        if mock_user_obj:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_owner_of_notification(func):
    """Decorator that is used for user authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id = request.args.get('userid', None)
        notification_id = request.view_args.get('notification_id', None)
        print(user_id, notification_id)

        if user_id is None or notification_id is None:
            flask_restful.abort(401)

        # check if the user is authenticated
        _, _ = get_authenticated_user()

        notification_profile_object = Notification.query.filter_by(id=notification_id, user_id=user_id).scalar()
        print(notification_profile_object)
        if notification_profile_object:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_admins(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        mock_user_obj, mock_user_roles = get_authenticated_user()
        print(mock_user_obj, mock_user_roles)

        if mock_user_obj and "administrator" in mock_user_roles:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_lifelong_learner(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id, mock_user_obj, mock_user_roles = check_if_profile_owner(*args, **kwargs)
        print(mock_user_obj, mock_user_roles)

        if mock_user_obj and \
                ("student" in mock_user_roles or "professor" in mock_user_roles or 'recruiter' in mock_user_roles):
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_recruiters_and_profile_owners(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_user_id_from_request()
        if user_id is None:
            user_id = get_user_id_from_cv_id_of_request()
        mock_user_obj, mock_user_roles = get_authenticated_user()

        if mock_user_obj.__dict__['id'] == int(user_id):
            return func(*args, **kwargs)
        else:
            if "recruiter" in mock_user_roles or "recruiting organisation" in mock_user_roles:
                recruiter_created_jobs = get_jobs_of_recruiter(mock_user_obj.__dict__['id'])
                user_applications_for_recruiter_jobs = has_applied_for_jobs(user_id, recruiter_created_jobs)
                if user_applications_for_recruiter_jobs and mock_user_obj:
                    return func(*args, **kwargs)
                else:
                    flask_restful.abort(401)
            else:
                flask_restful.abort(401)
    return wrapper

def only_profile_owners_and_recruiters_and_professors(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_user_id_from_request()
        mock_user_obj, mock_user_roles = get_authenticated_user()

        if mock_user_obj.__dict__['id'] == int(user_id):
            print("owner")
            return func(*args, **kwargs)
        elif "recruiter" in mock_user_roles or "recruiting organisation" in mock_user_roles:
            print("recr")
            recruiter_created_jobs = get_jobs_of_recruiter(mock_user_obj.__dict__['id'])
            user_applications_for_recruiter_jobs = has_applied_for_jobs(user_id, recruiter_created_jobs)
            if user_applications_for_recruiter_jobs and mock_user_obj:
                return func(*args, **kwargs)
            elif "professor" in mock_user_roles or "academic organisation" in mock_user_roles:
                professors_teaches_courses = get_courses_of_professor(mock_user_obj.__dict__['id'])
                user_courses_vs_professor_courses = attends_course(user_id, professors_teaches_courses)
                if user_courses_vs_professor_courses and mock_user_obj:
                    return func(*args, **kwargs)
                else:
                    flask_restful.abort(401)
            else:
                flask_restful.abort(401)
        elif "professor" in mock_user_roles or "academic organisation" in mock_user_roles:
            professors_teaches_courses = get_courses_of_professor(mock_user_obj.__dict__['id'])
            user_courses_vs_professor_courses = attends_course(user_id, professors_teaches_courses)
            if user_courses_vs_professor_courses and mock_user_obj:
                return func(*args, **kwargs)
            else:
                flask_restful.abort(401)

    return wrapper

def only_recruiters_and_recruitment_organizations(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user, roles = get_authenticated_user()

        if auth_user and ("recruiter" in roles or "recruiting organisation" in roles):
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)
    return wrapper


def only_recruiter_creator_of_job(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user, roles = get_authenticated_user()
        request_token = request.headers.get("Authorization", None)
        job_id = request.view_args.get('job_id', None)
        if job_id is None:
            job_id = request.args.get('jobid', None)
        if job_id is None:
            data = request.get_json()
            job_id=data['job_id']

        user_id = auth_user.__dict__['id']

        if request_token is None or user_id is None or job_id is None:
            flask_restful.abort(401)
        if not ("recruiter" in roles or "recruiting organisation" in roles):
            flask_restful.abort(401)

        job = Job.query.filter_by(id=job_id).scalar()
        creator_id = job.__dict__['creator_id']

        if creator_id == user_id:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_professors_or_academic_oranisations(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        mock_user_obj, mock_user_roles = get_authenticated_user()
        print(mock_user_obj, mock_user_roles)

        if mock_user_obj and ("professor" in mock_user_roles or "academic organisation" in mock_user_roles):
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_professor_or_academic_organisation_of_course(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user, roles = get_authenticated_user()
        request_token = request.headers.get("Authorization", None)
        course_id = request.view_args.get('course_id', None)
        if course_id is None:
            course_id = request.args.get('courseid', None)
        if course_id is None:
            data = request.get_json()
            course_id=data['course_id']

        user_id = auth_user.__dict__['id']

        if request_token is None or user_id is None or course_id is None:
            flask_restful.abort(401)
        if not ("professor" in roles or "academic organisation" in roles):
            flask_restful.abort(401)

        professor_course_object = UserCourse.query.filter_by(user_id=user_id, course_id=course_id, course_status='taught').scalar()
        print(professor_course_object)

        # todo: check if there is a relation between the course and the academic organisation

        if professor_course_object:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_authenticated(func):
    """Decorator that is used for user-role authentication and gives access to every authenticated user"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        u, r = get_authenticated_user()
        if u is None:
            flask_restful.abort(401)
        return func(*args, **kwargs)

    return wrapper


def only_profile_owner_or_professor_or_academic_organisation_of_course(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_user_id = get_user_id_from_request()
        auth_user, roles = get_authenticated_user()
        request_token = request.headers.get("Authorization", None)
        course_id = request.view_args.get('course_id', None)
        if course_id is None:
            course_id = request.args.get('courseid', None)
        if course_id is None:
            data = request.get_json()
            course_id=data['course_id']

        auth_user_id = auth_user.__dict__['id']

        if request_token is None or auth_user_id is None or request_user_id is None or course_id is None:
            flask_restful.abort(401)
        if auth_user_id == int(request_user_id):
            return func(*args, **kwargs)
        if not ("professor" in roles or "academic organisation" in roles):
            flask_restful.abort(401)

        professor_course_object = UserCourse.query.filter_by(user_id=auth_user_id, course_id=course_id, course_status='taught').scalar()
        print(professor_course_object)

        # todo: check if there is a relation between the course and the academic organisation

        if professor_course_object:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper
