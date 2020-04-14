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

from models import Book, User, Skill


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
                name=data['name']
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
            return jsonify(serialized_skills), 200
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


api.add_resource(UserObject, '/users')
api.add_resource(HandleUser, '/users/<user_id>')

api.add_resource(NewPassword, '/users/<user_id>/requestnewpassword')
api.add_resource(ChangePassword, '/users/<user_id>/updatePassword')

# Auth Routes
api.add_resource(Authentication, '/auth')

# Skill Routes
api.add_resource(SkillObject, '/skills')
api.add_resource(HandleSkill, '/skills/<skill_id>')
