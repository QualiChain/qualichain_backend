import argparse
import io
import secrets

import requests
from PIL import Image

import flask_restful
from flask import request

from application.models import User
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


def mock_response_from_inesc(user_token, user_id):
    """Mock response from INESC API"""

    # suppose there is INESC infrastructure send your token and get user details
    inesc_response = {"username": "panagiotis23", "role": "professor, student, recruiter, admin"}
    user_obj_exists = User.query.filter_by(userName=inesc_response["username"], id=user_id).scalar()
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
    request_token = request.headers.get("Authorization", None)
    user_id = request.view_args.get('user_id', None)
    if user_id is None:
        user_id = request.view_args.get('userid', None)
    if user_id is None:
        user_id = request.args.get('userid', None)
    if user_id is None:
        user_id = request.args.get('user_id', None)
    if user_id is None:
        data = request.get_json()
        user_id=data['user_id']

    if request_token is None or user_id is None:
        flask_restful.abort(401)

    mock_user_obj, mock_user_roles = mock_response_from_inesc(request_token, user_id)

    return user_id, mock_user_obj, mock_user_roles
