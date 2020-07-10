# =================================
#   User APIs
# =================================
import io
import logging
import os
import sys

from PIL import Image
from flask import request, jsonify, send_from_directory
from flask_mail import Message
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from application.database import db
from application.factory import mail
from application.models import User, UserCourse, UserCourseRecommendation, UserJob, UserJobRecommendation, \
    UserSkillRecommendation, \
    UserBadgeRelation, CV, Notification, UserAvatar, UserFile
from application.settings import MAIL_USERNAME, UPLOAD_FOLDER, APP_ROOT_PATH
from application.users import user_blueprint
from application.utils import generate_password, image_to_byte_array, allowed_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(user_blueprint)


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

    def delete(self, user_id):
        """ delete user """
        try:
            user_object = User.query.filter_by(id=user_id)
            if user_object.first():
                UserCourse.query.filter_by(user_id=user_id).delete()
                UserCourseRecommendation.query.filter_by(user_id=user_id).delete()
                UserJob.query.filter_by(user_id=user_id).delete()
                UserJobRecommendation.query.filter_by(user_id=user_id).delete()
                UserSkillRecommendation.query.filter_by(user_id=user_id).delete()
                UserBadgeRelation.query.filter_by(user_id=user_id).delete()
                CV.query.filter_by(user_id=user_id).delete()
                Notification.query.filter_by(user_id=user_id).delete()
                user_object.delete()
                db.session.commit()
                return "User with ID: {} deleted".format(user_id)
            else:
                return "User does not exist", 404
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


class ResetPassword(Resource):
    """This interface is used to implement Reset Password Functionality"""

    def post(self, username):
        data = dict(request.get_json())

        try:
            email = data['email']
            new_password = generate_password()

            user_object = User.query.filter_by(userName=username).first()
            user_object.set_password(new_password)
            db.session.commit()

            msg = Message('[QualiChain]: Your Password was reset', sender=MAIL_USERNAME, recipients=[email])
            msg.body = "Hello! \n\nYour new password is: `{}`.\n\n Best,\n The QualiChain Platform".format(new_password)
            mail.send(msg)
            return "New Password sent to".format(email)
        except Exception as ex:
            log.error(ex)


# =================================
#   User Avatar
# =================================


@user_blueprint.route('/upload/user/<userid>/avatar', methods=['POST'])
def upload_user_avatar(userid):
    """This function is the interface to upload user avatar"""
    try:
        image = request.files["image"]
        if image.filename == '':
            avatar = None
        else:
            image_from_pillow = Image.open(io.BytesIO(image.read()))
            avatar = image_to_byte_array(image_from_pillow)

        user_avatar = UserAvatar(
            user_id=userid,
            avatar=avatar
        )
        db.session.add(user_avatar)
        db.session.commit()
        return "avatar for user with ID: {} added".format(userid), 201
    except Exception as ex:
        log.error(ex)


@user_blueprint.route('/get/user/<userid>/avatar', methods=['GET'])
def get_user_avatar(userid):
    """Serves User with ID=`userid` avatar"""

    user_avatar_obj = UserAvatar.query.filter_by(user_id=userid).first()
    user_avatar = user_avatar_obj.avatar
    return {'avatar_in_bytes': str(user_avatar)}, 200


@user_blueprint.route('/user/<userid>/file-upload', methods=['POST'])
def upload_file(userid):
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        user_file = UserFile(
            user_id=userid,
            filename=file.filename
        )
        db.session.add(user_file)
        db.session.commit()

        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@user_blueprint.route('/user/<userid>/files', methods=['GET'])
def list_user_files(userid):
    """This interface is used to retrieve the list of user files"""
    try:
        files = UserFile.query.filter_by(user_id=userid)
        list_of_files = [file.filename for file in files]
        return {'files': list_of_files}, 200
    except Exception as ex:
        log.error(ex)


@user_blueprint.route('/download/<filename>', methods=['GET'])
def retrieve_file(filename):
    """This interface is used to retrieve provided file"""
    uploads = os.path.join(APP_ROOT_PATH, UPLOAD_FOLDER)
    return send_from_directory(directory=uploads, filename=filename)



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


api.add_resource(UserObject, '/users')
api.add_resource(HandleUser, '/users/<user_id>')

api.add_resource(NewPassword, '/users/<user_id>/requestnewpassword')
api.add_resource(ChangePassword, '/users/<user_id>/updatePassword')
api.add_resource(ResetPassword, '/user/<username>/resetPassword')

# Auth Routes
api.add_resource(Authentication, '/auth')
