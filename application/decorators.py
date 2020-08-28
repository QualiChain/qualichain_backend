from functools import wraps

import flask_restful
from flask import request

from application.utils import mock_response_from_inesc
from application.models import User, UserCourse


def only_profile_owner(func):
    """Decorator that is used for user authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        request_token = request.headers.get("Authorization", None)
        user_id = request.view_args.get('user_id', None)
        if user_id is None:
            user_id = request.args.get('user_id', None)

        if request_token is None or user_id is None:
            flask_restful.abort(401)

        mock_user_obj, mock_user_roles = mock_response_from_inesc(request_token, user_id)
        if mock_user_obj:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper

def only_professors(func):
    """Decorator that is used for user-role authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        request_token = request.headers.get("Authorization", None)
        user_id = request.view_args.get('user_id', None)
        if user_id is None:
            user_id = request.args.get('user_id', None)
        if request_token is None or user_id is None:
            flask_restful.abort(401)

        mock_user_obj, mock_user_roles = mock_response_from_inesc(request_token, user_id)
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
        user_id = request.args.get('user_id', None)
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

        request_token = request.headers.get("Authorization", None)
        user_id = request.view_args.get('user_id', None)
        if user_id is None:
            user_id = request.args.get('user_id', None)
        if request_token is None or user_id is None:
            flask_restful.abort(401)

        mock_user_obj, mock_user_roles = mock_response_from_inesc(request_token, user_id)
        print(mock_user_obj, mock_user_roles)
        if mock_user_obj and "student" in mock_user_roles:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper
