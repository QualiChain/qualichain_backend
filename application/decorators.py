from functools import wraps

import flask_restful
from flask import request

from application.utils import mock_response_from_inesc, check_if_profile_owner
from application.models import User, UserCourse, Job, Notification

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

def only_professors(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id, mock_user_obj, mock_user_roles = check_if_profile_owner(*args, **kwargs)
        print(mock_user_obj, mock_user_roles)

        if mock_user_obj and "professor" in mock_user_roles:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper

def only_professor_of_course(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_token = request.headers.get("Authorization", None)
        course_id = request.view_args.get('course_id', None)
        if course_id is None:
            course_id = request.args.get('courseid', None)
        if course_id is None:
            data = request.get_json()
            course_id=data['course_id']
        user_id = request.args.get('userid', None)
        print(user_id, course_id)

        if request_token is None or user_id is None or course_id is None:
            flask_restful.abort(401)

        professor_course_object = UserCourse.query.filter_by(user_id=user_id, course_id=course_id, course_status='taught').scalar()
        print(professor_course_object)
        if professor_course_object:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_students(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id, mock_user_obj, mock_user_roles = check_if_profile_owner(*args, **kwargs)
        print(mock_user_obj, mock_user_roles)

        if mock_user_obj and "student" in mock_user_roles:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper

def only_recruiters(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id, mock_user_obj, mock_user_roles = check_if_profile_owner(*args, **kwargs)
        print(mock_user_obj, mock_user_roles)

        if mock_user_obj and "recruiter" in mock_user_roles:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper


def only_recruiters_of_job(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        job_id = request.view_args.get('job_id', None)
        user_id = request.args.get('userid', None)
        print(user_id, job_id)

        if user_id is None or job_id is None:
            flask_restful.abort(401)

        recruiter_job_object = Job.query.filter_by(id=job_id, creator_id=user_id).scalar()
        print(recruiter_job_object)
        if recruiter_job_object:
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

        notification_profile_object = Notification.query.filter_by(id=notification_id, user_id=user_id).scalar()
        print(notification_profile_object)
        if notification_profile_object:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)


    return wrapper
