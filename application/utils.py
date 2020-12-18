import argparse
import io
import secrets

import requests
from PIL import Image

from application.models import User, Kpi
from application.settings import ALLOWED_EXTENSIONS, RABBITMQ_HOST, RABBITMQ_MNG_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD, \
    API_HOST, API_PORT
from application.database import db


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
    inesc_response = {"username": "kapsali29", "role": "some-role"}
    user_obj_exists = User.query.filter_by(userName=inesc_response["username"], id=user_id).scalar()
    return user_obj_exists


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


def kpi_measurement(kpi_name):
    try:
        kpi_obj = Kpi.query.filter_by(kpi_name=kpi_name)
        kpi_obj_exists = kpi_obj.scalar()

        if not kpi_obj_exists:
            kpi_obj = Kpi(kpi_name=kpi_name, count=1)
            db.session.add(kpi_obj)
            db.session.commit()
            print('KpiObject with name= {} has been added'.format(kpi_name))
        else:
            kpi_obj[0].count = kpi_obj[0].count + 1
            db.session.commit()
            print('KpiObject with name= {} has been updated'.format(kpi_name))
    except Exception as ex:
        print('Could not measure the KPI', ex)
