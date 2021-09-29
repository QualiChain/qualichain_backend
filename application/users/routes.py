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
from application.decorators import only_profile_owner, only_authenticated, \
    only_profile_owners_and_recruiters_and_professors
from application.factory import mail
from application.models import User, UserCourse, UserCourseRecommendation, UserApplication, UserJobRecommendation, \
    UserSkillRecommendation, UserRecruitmentOrganisation, UserAcademicOrganisation, \
    UserBadgeRelation, CV, Notification, UserAvatar, UserFile, UserNotificationPreference, Thesis, ThesisRequest, Job, \
    JobSkill
from application.settings import MAIL_USERNAME, UPLOAD_FOLDER, APP_ROOT_PATH, IAM_API_KEYS
from application.users import user_blueprint
from application.utils import generate_password, image_to_byte_array, allowed_file, kpi_measurement, add_new_QC_user, \
    create_user_solid_pod, produce_user_id_to_KBZ

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
            user_password = data['password']

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

            user.set_password(user_password)
            db.session.commit()
            kpi_measurement('create_user')
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

    # method_decorators = {'put': [only_profile_owner], 'delete': [only_profile_owner],
    #                      'get': [only_profile_owners_and_recruiters_and_professors]
    #                      }

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
                UserApplication.query.filter_by(user_id=user_id).delete()
                jobs = Job.query.filter_by(creator_id=user_id)
                if jobs.first():
                    for job in jobs:
                        UserApplication.query.filter_by(job_id=job.id).delete()
                        JobSkill.query.filter_by(job_id=job.id).delete()
                jobs.delete()
                UserJobRecommendation.query.filter_by(user_id=user_id).delete()
                UserSkillRecommendation.query.filter_by(user_id=user_id).delete()
                UserBadgeRelation.query.filter_by(user_id=user_id).delete()
                CV.query.filter_by(user_id=user_id).delete()
                UserAvatar.query.filter_by(user_id=user_id).delete()
                Notification.query.filter_by(user_id=user_id).delete()
                UserNotificationPreference.query.filter_by(user_id=user_id).delete()
                UserAcademicOrganisation.query.filter_by(user_id=user_id).delete()
                UserRecruitmentOrganisation.query.filter_by(user_id=user_id).delete()
                thesis = Thesis.query.filter_by(professor_id=user_id)
                if thesis.first():
                    Thesis.query.filter_by(professor_id=user_id).delete()
                theses = Thesis.query.filter_by(student_id=user_id)
                if theses.first():
                    for thesis_obj in theses:
                        thesis_obj.student_id = None
                        thesis_obj.status = 'published'
                ThesisRequest.query.filter_by(student_id=user_id).delete()
                UserFile.query.filter_by(user_id=user_id).delete()
                user_object.delete()
                db.session.commit()
                produce_user_id_to_KBZ(user_id=user_id)
                return "User with ID: {} deleted".format(user_id)
            else:
                return "User does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class ThesisObject(Resource):
    """This class is used to create and get list of thesis objects"""

    def post(self):
        """
        Create a new Thesis
        """
        data = request.get_json()
        try:
            thesis_title = data['title']
            professor_id = data['professor_id']
            thesis_description = data['description']

            thesis = Thesis(professor_id=professor_id, title=thesis_title, description=thesis_description)
            db.session.add(thesis)
            db.session.commit()

            db.session.commit()
            kpi_measurement('create_thesis')
            return "New Thesis added. Thesis={}".format(thesis.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """
        Get list of Thesis Objects
        """

        arguments = {}
        if request.args.get('professor_id') is not None:
            arguments['professor_id'] = request.args.get('professor_id')
        if request.args.get('student_id') is not None:
            arguments['student_id'] = request.args.get('student_id')
        if request.args.get('status') is not None:
            arguments['status'] = request.args.get('status')

        try:
            thesis_objs = Thesis.query.filter_by(**arguments)
            serialized_thesis_objs = [th.serialize() for th in thesis_objs]
            return jsonify(serialized_thesis_objs)

        except Exception as ex:
            log.error(ex)


class HandleThesis(Resource):
    """This class is used to handle the thesis objects"""

    def get(self, thesis_id):
        """
        Get thesis
        """
        try:
            thesis_object = Thesis.query.filter_by(id=thesis_id).first()
            serialized_thesis = thesis_object.serialize()
            return serialized_thesis
        except Exception as ex:
            log.info(ex)
            return "Thesis with ID: {} does not exist".format(thesis_id), 404

    def put(self, thesis_id):
        """
        Update thesis data
        """
        data = dict(request.get_json())

        try:
            thesis_object = Thesis.query.filter_by(id=thesis_id)
            thesis_object.update(data)
            status = data['status']
            student_id = data['student_id']

            thesis_obj = Thesis.query.filter_by(id=thesis_id).first()
            thesis_name = thesis_obj.title

            if status == 'assigned':
                message = "Your application for the thesis {} has been accepted.".format(thesis_name)
                request_notification = Notification(user_id=student_id, message=message)
                db.session.add(request_notification)
            elif status == 'completed':
                message = "You have completed the thesis {}".format(thesis_name)
                request_notification = Notification(user_id=student_id, message=message)
                db.session.add(request_notification)

            db.session.commit()
            return "Thesis with ID: {} updated".format(thesis_id)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, thesis_id):
        """ delete thesis """
        try:
            thesis_object = Thesis.query.filter_by(id=thesis_id)
            if thesis_object.first():
                ThesisRequest.query.filter_by(thesis_id=thesis_id).delete()
                thesis_object.delete()
                db.session.commit()
                return "Thesis with ID: {} deleted".format(thesis_id)
            else:
                return "Thesis does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class HandleThesisRequest(Resource):
    """This class is used to handle the thesis request objects"""

    def get(self):
        """
        Get thesis request objects
        """

        if request.args.get('thesis_id') is not None:
            thesis_id = request.args.get('thesis_id')
            try:
                thesis_objects = ThesisRequest.query.filter_by(thesis_id=thesis_id)
                serialized_thesis_request_objs = [th.serialize() for th in thesis_objects]
                return serialized_thesis_request_objs
            except Exception as ex:
                log.info(ex)
                return "Thesis with ID: {} does not exist".format(thesis_id), 404
        else:
            return "No Thesis ID provided in the request", 404

    def post(self):
        """
        Create a new Thesis Request
        """
        data = request.get_json()
        try:
            thesis_id = data['thesis_id']
            student_id = data['student_id']

            thesis_request = ThesisRequest(student_id=student_id, thesis_id=thesis_id)
            db.session.add(thesis_request)
            thesis_obj = Thesis.query.filter_by(id=thesis_id).first()
            professor_id = thesis_obj.professor_id
            student_name = User.query.filter_by(id=student_id).first().fullName
            thesis_name = thesis_obj.title
            message = "Student {} has applied for thesis: {}".format(student_name, thesis_name)
            request_notification = Notification(user_id=professor_id, message=message)
            db.session.add(request_notification)
            db.session.commit()

            return "New Thesis Request added. Thesis Request={}".format(thesis_request.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def delete(self):
        """ delete thesis request"""
        if request.args.get('thesis_request_id') is not None:
            thesis_request_id = request.args.get('thesis_request_id')
            try:
                thesis_request_object = ThesisRequest.query.filter_by(id=thesis_request_id)
                if thesis_request_object.first():
                    thesis_request_object.delete()
                    db.session.commit()
                    return "Thesis request with ID: {} deleted".format(thesis_request_id)
                else:
                    return "Thesis request does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex
        else:
            return "No Thesis Request ID provided in the request", 404



api.add_resource(ThesisObject, '/thesis')
api.add_resource(HandleThesis, '/thesis/<thesis_id>')
api.add_resource(HandleThesisRequest, '/thesis_request')

class NewPassword(Resource):
    """This class is used to set user's password"""

    method_decorators = {'post': [only_profile_owner]}

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

    method_decorators = {'post': [only_profile_owner]}

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
@only_profile_owner
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
@only_authenticated
def get_user_avatar(userid):
    """Serves User with ID=`userid` avatar"""

    user_avatar_obj = UserAvatar.query.filter_by(user_id=userid).first()
    user_avatar = user_avatar_obj.avatar
    return {'avatar_in_bytes': str(user_avatar)}, 200


@user_blueprint.route('/user/<userid>/file-upload', methods=['POST'])
@only_profile_owner
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
        file_name = '{}_{}'.format(str(userid), file.filename)
        file_exists = UserFile.query.filter_by(filename=file_name).scalar()
        if not file_exists:
            # filename = secure_filename(file_name)
            filepath = "{}/{}".format(UPLOAD_FOLDER, file_name)
            file.save(filepath)

            user_file = UserFile(
                user_id=userid,
                filename=file_name
            )
            db.session.add(user_file)
            db.session.commit()

            resp = jsonify({'message': 'File successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(
                {'message': 'The file name you selected already exists. Please change the name of the uploaded file.'})
            resp.status_code = 400
            return resp

    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@user_blueprint.route('/user/<userid>/files', methods=['GET'])
@only_profile_owner
def list_user_files(userid):
    """This interface is used to retrieve the list of user files"""
    try:
        files = UserFile.query.filter_by(user_id=userid)
        list_of_files = [{'filename': file.filename, 'file_id': file.id} for file in files]
        return {'files': list_of_files}, 200
    except Exception as ex:
        log.error(ex)


@user_blueprint.route('/delete/user/<userid>/files/<file_name>', methods=['DELETE'])
@only_profile_owner
def delete_user_file(userid, file_name):
    """This interface is used to delete a file"""
    try:
        files = UserFile.query.filter_by(user_id=userid, filename=file_name)
        files_exist = files.scalar()
        if files_exist:
            files.delete()
            os.remove(os.path.join(UPLOAD_FOLDER, file_name))
            db.session.commit()
            return "File {} of user {} deleted".format(file_name, userid)
        else:
            return "File does not exist", 404
    except Exception as ex:
        log.error(ex)
        return ex


@user_blueprint.route('/delete/user/<userid>/files/id/<file_id>', methods=['DELETE'])
@only_profile_owner
def delete_user_file_using_id(userid, file_id):
    """This interface is used to delete a file"""
    try:
        files = UserFile.query.filter_by(user_id=userid, id=file_id)
        files_exist = files.scalar()
        if files_exist:
            file_name = files[0].filename
            files.delete()
            os.remove(os.path.join(UPLOAD_FOLDER, file_name))
            db.session.commit()
            return "File {} of user {} deleted".format(file_name, userid)
        else:
            return "File does not exist", 404
    except Exception as ex:
        log.error(ex)
        return ex


@user_blueprint.route('/download/<filename>', methods=['GET'])
@only_profile_owner
def retrieve_file(filename):
    """This interface is used to retrieve provided file"""
    uploads = os.path.join(APP_ROOT_PATH, UPLOAD_FOLDER)
    return send_from_directory(directory=uploads, filename=filename)


@user_blueprint.route('/download/file/<file_id>', methods=['GET'])
@only_profile_owner
def retrieve_using_file_id(file_id):
    files = UserFile.query.filter_by(id=file_id)
    files_exist = files.scalar()
    if files_exist:
        filename = files[0].filename
        uploads = os.path.join(APP_ROOT_PATH, UPLOAD_FOLDER)
        return send_from_directory(directory=uploads, filename=filename)
    else:
        return "File does not exist", 404


@user_blueprint.route('/get/user/by/email', methods=['POST'])
def get_user_by_email():
    data = request.get_json()
    email = data['email']
    api_key = request.headers.get('API_KEY', None)
    if api_key:
        if api_key in list(IAM_API_KEYS.values()):
            user = User.query.filter_by(email=email)
            if_user_exists = user.scalar()
            if if_user_exists:
                get_user_data = user.first().serialize()
                return get_user_data, 201
            else:
                user = add_new_QC_user(data)
                return user, 201
        else:
            return {'msg': "Access Denied"}, 403
    else:
        return {'msg': "Access Denied"}, 403


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


class UserPermissions(Resource):
    def get(self):
        """
        Get user permissions
        """
        user_permissions = {
            'view_courses': ['student', 'employee', 'professor', 'administrator'],
            'add_course': ['professor', 'academic organisation', 'administrator'],
            'edit_course': ['professor', 'academic organisation', 'administrator'],
            'delete_course': ['professor', 'academic organisation', 'administrator'],
            'view_jobs': ['student', 'employee', 'recruiter', 'recruitment organisation',
                          'administrator'],
            'add_job_post': ['recruiter', 'recruitment organisation', 'administrator'],
            'edit_job_post': ['recruiter', 'recruitment organisation', 'administrator'],
            'delete_job_post': ['recruiter', 'recruitment organisation', 'administrator'],
            'view_profiles': ['professor', 'recruiter', 'academic organisation',
                              'recruitment organisation', 'administrator'],
            'add_profile': ['administrator'],
            'view_own_profile': ['student', 'professor', 'recruiter', 'life long learner',
                                 'academic organisation', 'recruitment organisation', 'employee',
                                 'job seeker', 'administrator'],
            'edit_own_profile': ['student', 'professor', 'recruiter', 'life long learner',
                                 'academic organisation', 'recruitment organisation', 'employee',
                                 'job seeker', 'administrator'],
            'delete_own_profile': ['student', 'professor', 'recruiter', 'life long learner',
                                   'academic organisation', 'recruitment organisation', 'employee',
                                   'job seeker', 'administrator'],
            'view_other_profile': ['professor', 'recruiter', 'academic organisation',
                                   'recruitment organisation', 'job seeker', 'administrator'],
            'edit_other_profile': ['professor', 'administrator'],
            'delete_other_profile': ['administrator'],
            'view_recruitment': ['recruiter', 'recruitment organisation', 'administrator'],
            'access_MCDSS': ['student', 'recruiter', 'recruitment organisation', 'administrator', 'professor',
                             'academic organisation'],
            'view_skills': ['student', 'professor', 'recruiter', 'life long learner', 'employee', 'job seeker',
                            'administrator'],
            'upload_own_files': ['student', 'professor', 'recruiter', 'life long learner', 'employee', 'job seeker',
                                 'administrator'],
            'retrieve_own_files': ['student', 'professor', 'recruiter', 'life long learner', 'employee', 'job seeker',
                                   'administrator'],
            'delete_own_files': ['student', 'professor', 'recruiter', 'life long learner', 'employee', 'job seeker',
                                 'administrator'],
            'get_their_job_applications': ["student", "professor", "life long learner", "employee",
                                           "job seeker", "administrator"],
            'get_job_recommendations': ["student", "life long learner", "employee",
                                        "job seeker", "administrator"],
            'manage_own_notifications': ['student', 'professor', 'recruiter', 'life long learner', 'employee',
                                         'job seeker', 'administrator'],
            'manage_own_notifications_preferences': ['student', 'professor', 'recruiter', 'life long learner',
                                                     'employee', 'job seeker', 'administrator'],
            'apply_for_a_job_position': ["student", "life long learner", "employee",
                                         "job seeker", "administrator"],
            'get_courses_recomendations': ["student", "life long learner", "employee",
                                           "job seeker", "administrator"],
            'get_skills_recomendations': ["student", "life long learner", "employee",
                                          "job seeker", "administrator"],
            'add_and_update_thesis': ["professor", "administrator"],
            'view_thesis_subjects': ["student", "professor", "administrator"],
            'create_smart_badge': ['academic organisation', 'professor', 'administrator'],
            'issue_smart_badge': ['academic organisation', 'professor', 'administrator'],
            'verify_smart_badge': ['student', 'professor', 'recruiter', 'life long learner', 'academic organisation',
                                   'recruitment organisation', 'employee', 'job seeker', 'administrator']

        }
        return jsonify(user_permissions)


api.add_resource(UserPermissions, '/user_permissions')
