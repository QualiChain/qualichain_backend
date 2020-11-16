import argparse
import io
import secrets

import requests
from PIL import Image

import flask_restful
from flask import request

from application.models import User, CV, UserFile
from application.settings import ALLOWED_EXTENSIONS, RABBITMQ_HOST, RABBITMQ_MNG_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD


def image_to_byte_array(image: Image):
    """This function is used to save user avatar to Postgresql"""
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def allowed_file(filename):
    """Allowed formats to be uploaded on QC db"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_password(pwd_length=8):
    """This function is used to generate a random password with length=8"""
    random_password = secrets.token_hex(pwd_length)
    return random_password


def get_authenticated_user():
    """ Get user from access token if exists, otherwise abort"""
    request_token = request.headers.get("Authorization", None)
    user, roles = mock_response_from_inesc(request_token)
    if user is None:
        print("No such user")
        flask_restful.abort(401)

    return user, roles


def mock_response_from_inesc(user_token):
    """Mock response from INESC API"""
    # suppose there is INESC infrastructure send your token and get user details
    inesc_response = {"username": "panagiotis31", "role": "professor, student, recruiter, admin, lifelong learner, academic organisation"}
    user_obj_exists = User.query.filter_by(userName=inesc_response["username"]).scalar()
    return user_obj_exists, inesc_response["role"]


def create_vhost(new_vhost):
    """This function is used to create a vhost on RabbitMQ"""
    headers = {
        'content-type': 'application/json',
    }

    response = requests.put(
        'http://{}:{}/api/vhosts/{}'.format(RABBITMQ_HOST, RABBITMQ_MNG_PORT, new_vhost),
        headers=headers,
        auth=(RABBITMQ_USER, RABBITMQ_PASSWORD)
    )
    return response


def assign_grade(course_status, grade):
    """This function is used to set user's grade for specific course"""
    grades_list = [*range(0, 11, 1)]
    if course_status == 'done':
        if grade:
            if grade in grades_list:
                return grade
            else:
                return 0
        else:
            return 0
    else:
        return 0


def assign_skill_level(skill_level):
    """This function is used to define user's skill level"""
    skill_level_list = [*range(0, 11, 1)]
    if skill_level:
        if skill_level in skill_level_list:
            return skill_level
        else:
            return None
    return None


def parse_arguments():
    """This function is used to parse Command Line Args"""
    arg_parser = argparse.ArgumentParser(
        description="Instructs Esco loader to get Esco skills file path")
    arg_parser.add_argument("--path", help="Esco Skills file path")
    return arg_parser


def check_if_profile_owner(*args, **kwargs):
    """ Checks if the user is indeed the profile owner """
    authenticated_user, roles = get_authenticated_user()
    request_token = request.headers.get("Authorization", None)
    user_id = get_user_id_from_request()
    if user_id is None:
        user_id = get_user_id_from_cv_id_of_request()
    if user_id is None:
        user_id = get_user_id_from_file_id_of_request()
    if user_id is None:
        user_id = get_user_id_from_filename_of_request()

    if request_token is None or user_id is None:
        flask_restful.abort(401)

    if authenticated_user.__dict__['id'] != int(user_id):
        print(""" User is authenticated but is not the profile owner""")
        flask_restful.abort(401)

    return user_id, authenticated_user, roles


def get_user_id_from_request():
    user_id = request.view_args.get('user_id', None)
    if user_id is None:
        user_id = request.view_args.get('userid', None)
    if user_id is None:
        user_id = request.args.get('userid', None)
    if user_id is None:
        user_id = request.args.get('user_id', None)
    if user_id is None:
        data = request.get_json()
        if data is None:
            user_id = None
        elif 'user_id' in data:
            user_id = data['user_id']
    return user_id


def get_user_id_from_cv_id_of_request():
    cv_id = request.view_args.get('cv_id', None)
    if cv_id is None:
        return cv_id
    else:
        cv = CV.query.get(cv_id)
        return cv.user_id

def get_user_id_from_file_id_of_request():
    file_id = request.view_args.get('file_id', None)
    if file_id is None:
        return file_id
    else:
        file = UserFile.query.get(file_id)
        return file.user_id

def get_user_id_from_filename_of_request():
    filename = request.view_args.get('filename', None)
    if filename is None:
        return filename
    else:
        file = UserFile.query.filter_by(filename=filename).scalar()
        return file.user_id
