import argparse
import io
import secrets
import json
import requests
from PIL import Image

import flask_restful
from flask import request

from application.clients.rabbitmq_client import RabbitMQClient
from application.models import User, Kpi, CV, UserFile, UserNotificationPreference, Notification, Job, UserApplication, \
    UserCourse, KpiTime, AcademicOrganisation, UserAcademicOrganisation, RecruitmentOrganisation, \
    UserRecruitmentOrganisation

from application.settings import ALLOWED_EXTENSIONS, RABBITMQ_HOST, RABBITMQ_MNG_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD, \
    KBZ_QUEUE
from application.database import db

IAM_ENDPOINT = 'https://qualichain.herokuapp.com/auth/validateToken'


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
    user, roles = get_qc_user_from_token(request_token)
    if user is None:
        print("No such user")
        flask_restful.abort(401)

    return user, roles


def mock_response_from_inesc(user_token):
    """Mock response from INESC API"""
    # suppose there is INESC infrastructure send your token and get user details
    inesc_response = {"username": "panagiotis33",
                      "role": "professor, student, recruiter, admin, lifelong learner, academic organisation"}
    user_obj_exists = User.query.filter_by(userName=inesc_response["username"]).scalar()
    return user_obj_exists, inesc_response["role"]


def get_qc_user_from_token(token):
    user_json = get_authenticated_user_from_token(token)
    user = None
    roles = None
    if user_json is not None:
        user = User.query.filter_by(email=user_json["email"]).first()
        print(user)
        # if user is authenticated through IAM but not a QC user create this user
        if user.solid_pod is False:
            solid_response = create_user_solid_pod(user_json, token)
            print(solid_response)
        roles = user_json['roles']
    return user, roles


def get_authenticated_user_from_token(token):
    if token is None:
        return None
    response = requests.post(IAM_ENDPOINT, auth=BearerAuth(token))
    if response.status_code == 200:
        return json.loads(response.text)['response_data']
    return None


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
    if user_id is None:
        user_id = get_user_id_from_notification_preference_of_request()
    if user_id is None:
        user_id = get_user_id_from_notification_of_request()

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


def get_jobs_of_recruiter(recruiter_id):
    recruiter_jobs = Job.query.filter_by(creator_id=recruiter_id)
    job_ids = [r.__dict__["id"] for r in recruiter_jobs]
    return job_ids


def get_courses_of_professor(professor_id):
    professor_courses = UserCourse.query.filter_by(user_id=professor_id, course_status="taught")
    course_ids = [p.__dict__["course_id"] for p in professor_courses]
    return course_ids


def has_applied_for_jobs(user_id, job_ids):
    user_job_applications = UserApplication.query.filter_by(user_id=user_id)
    applied_job_ids = [a.__dict__["job_id"] for a in user_job_applications]
    jobs_in_common = set(applied_job_ids) & set(job_ids)
    print(jobs_in_common)
    return len(jobs_in_common) > 0


def attends_course(user_id, courses_id):
    user_courses = UserCourse.query.filter_by(user_id=user_id)
    user_courses_ids = [u.__dict__["course_id"] for u in user_courses]
    courses_in_common = set(user_courses_ids) & set(courses_id)
    return courses_in_common


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


def get_user_id_from_notification_preference_of_request():
    preference_id = request.args.get('preference_id', None)
    if preference_id is None:
        return preference_id
    else:
        preference = UserNotificationPreference.query.get(preference_id)
        return preference.user_id


def get_user_id_from_notification_of_request():
    notification_id = request.view_args.get('notification_id', None)
    if notification_id is None:
        return notification_id
    else:
        notification = Notification.query.get(notification_id)
        return notification.user_id


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = self.token
        return r


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


def kpi_time_measurement(kpi_name, time):
    try:
        kpi_obj = KpiTime(kpi_name=kpi_name, time=time)
        db.session.add(kpi_obj)
        db.session.commit()
        print('KpiTimeObject with name= {} has been added. Time: {} microseconds'.format(kpi_name, time))
    except Exception as ex:
        print('Could not measure the KPI', ex)


def add_new_QC_user(data):
    store_new_user(data)
    kpi_measurement('create_user')
    user = User.query.filter_by(email=data["email"]).first()
    store_user_organizations(data, user)
    return user.serialize()


def store_new_user(data):
    user = User(
        userPath='',
        role=data['roles'][0],
        pilotId=1,
        userName=data['name'],
        fullName=data['name'],
        name=data['name'],
        surname=data['name'],
        gender='unknown',
        birthDate="",
        country="",
        city="",
        address="",
        zipCode="",
        mobilePhone="",
        homePhone="",
        email=data['email']
    )
    db.session.add(user)
    db.session.commit()


def store_user_organizations(data, user):
    organizations = data['organizations']
    for o in organizations:
        a_org = AcademicOrganisation.query.filter_by(title=o).first()

        if a_org is not None:
            acad_organization_id = a_org.id
            user_organisation_obj = UserAcademicOrganisation(
                user_id=user.id,
                organisation_id=acad_organization_id
            )
            db.session.add(user_organisation_obj)
            db.session.commit()

        r_org = RecruitmentOrganisation.query.filter_by(title=o).first()
        if r_org is not None:
            recr_organization_id = r_org.id
            user_organisation_obj = UserRecruitmentOrganisation(
                user_id=user.id,
                organisation_id=recr_organization_id
            )
            db.session.add(user_organisation_obj)
            db.session.commit()


def create_user_solid_pod(data, token):
    solid_pod_url = 'https://solid.qualichain-project.eu/pods'
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"}
    body_data = {
        "login": "qualichain" + data['id'],
        "webId": "https://solid.qualichain-project.eu/webid/" + data['id'] + "#me",
        "name": data['name']
    }
    jsonified_body_data = json.dumps(body_data)
    response = requests.request("POST", solid_pod_url, data=jsonified_body_data, headers=headers)
    print(response.text)
    return response


def produce_user_id_to_KBZ(user_id):
    """This function is used to produce user id after user deletion to KBZ via AMQP"""
    rabbitmq_client = RabbitMQClient()
    user_id_dict = {'user_id': user_id}
    json_data = json.dumps(user_id_dict)
    rabbitmq_client.producer(queue=KBZ_QUEUE, message=json_data)
