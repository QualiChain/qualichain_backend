# =================================
#   Organisations APIs
# =================================
import logging
import sys

from flask import request, jsonify
from flask_restful import Resource, Api

from application.database import db
from application.models import AcademicOrganisation, RecruitmentOrganisation, UserAcademicOrganisation, \
    UserRecruitmentOrganisation
from application.organisations import organisation_blueprint

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(organisation_blueprint)


class AcademicOrganisationObject(Resource):
    """
    This object is used to:

    1) Create a new Academic Organisation
    2) Get all stored academic organisations
    """

    def post(self):
        """
        Append new academic organisation
        """
        data = request.get_json()

        try:
            organisation = AcademicOrganisation(
                title=data['title'],
                description=data['description']
            )

            db.session.add(organisation)
            db.session.commit()
            return "Academic Organisation added - id={}".format(organisation.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """
        Get All Academic Organisations
        """
        try:
            organisations = AcademicOrganisation.query.all()
            serialized_organisations = [organisation.serialize() for organisation in organisations]
            return jsonify(serialized_organisations)

        except Exception as ex:
            log.error(ex)


class HandleAcademicOrganisation(Resource):
    """This class is used to get or edit a specified Academic organisation"""

    def get(self, organisation_id):
        """
        Get specific academic organisation
        """
        try:
            organisation_object = AcademicOrganisation.query.filter_by(id=organisation_id).first()
            serialized_organisation = organisation_object.serialize()
            return jsonify(serialized_organisation)
        except Exception as ex:
            log.error(ex)
            return ex

    def put(self, organisation_id):
        """
        Update academic organisation
        """
        data = dict(request.get_json())

        try:
            organisation_object = AcademicOrganisation.query.filter_by(id=organisation_id)
            if len(data) != 0:
                organisation_object.update(data)
                db.session.commit()
            return "Organisation with ID: {} updated".format(organisation_id)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, organisation_id):
        """ delete academic organisation """
        try:
            organisation_object = AcademicOrganisation.query.filter_by(id=organisation_id)
            if organisation_object.first():
                UserAcademicOrganisation.query.filter_by(organisation_id=organisation_id).delete()
                organisation_object.delete()
                db.session.commit()
                return "Organisation with ID: {} deleted".format(organisation_id)
            else:
                return "Organisation does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class UserAcademicOrganisationObject(Resource):
    """
    This object is used to:

    1) Create a new User - Academic Organisation relationship
    """

    def post(self):
        """
        Append new user - academic organisation relationship
        """
        data = request.get_json()

        try:
            user_organisation_obj = UserAcademicOrganisation(
                user_id=data['user_id'],
                organisation_id=data['academic_organisation_id']
            )

            db.session.add(user_organisation_obj)
            db.session.commit()
            return "User - Academic Organisation Object added.", 201

        except Exception as ex:
            log.error(ex)
            return ex, 400


class HandleUserAcademicOrganisation(Resource):
    """This class is used to get, delete a  User Academic organisation objects related to given organisation"""

    def get(self, organisation_id):
        """
        Get specific user academic organisation relationship with given org id
        """
        try:
            organisation_objects = UserAcademicOrganisation.query.filter_by(organisation_id=organisation_id)
            serialized_organisations = [organisation.serialize() for organisation in
                                        organisation_objects]
            return jsonify(serialized_organisations)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, organisation_id):
        """ delete user academic organisation objects related to given org id"""
        try:
            organisation_objects = UserAcademicOrganisation.query.filter_by(organisation_id=organisation_id)
            if organisation_objects.first():
                organisation_objects.delete()
                db.session.commit()
                return "UserOrganisation objects related to organisation with id={} deleted".format(organisation_id)
            else:
                return "Organisation does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class HandleAcademicUsers(Resource):
    """This class is used to get, delete a  User Academic organisation objects related to given user"""

    def get(self, user_id):
        """
        Get specific user academic organisation relationship with given user id
        """
        try:
            objects = UserAcademicOrganisation.query.filter_by(user_id=user_id)
            serialized_obj = [obj.serialize() for obj in objects]
            return jsonify(serialized_obj)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, user_id):
        """ delete user academic organisation objects related to given user id"""
        try:
            objects = UserAcademicOrganisation.query.filter_by(user_id=user_id)
            if objects.first():
                objects.delete()
                db.session.commit()
                return "UserOrganisation objects related to user with id={} deleted".format(user_id)
            else:
                return "User does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class AcademicOrgansiationUserRelationship(Resource):
    """This class is used to get, delete a specific User Academic organisation object"""

    def get(self, relation_id):
        """
        Get specific user academic organisation relationship with given id
        """
        try:
            object = UserAcademicOrganisation.query.filter_by(id=relation_id).first()
            serialized_obj = object.serialize()
            return jsonify(serialized_obj)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, relation_id):
        """ delete user academic organisation objects related to given id"""
        try:
            object = UserAcademicOrganisation.query.filter_by(id=relation_id).first()
            if object:
                object.delete()
                db.session.commit()
                return "UserOrganisation object with id={} deleted".format(relation_id)
            else:
                return "Object does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class RecruitmentOrganisationObject(Resource):
    """
    This object is used to:

    1) Create a new Recruitment Organisation
    2) Get all stored Recruitment organisations
    """

    def post(self):
        """
        Append new Recruitment organisation
        """
        data = request.get_json()

        try:
            organisation = RecruitmentOrganisation(
                title=data['title'],
                description=data['description']
            )

            db.session.add(organisation)
            db.session.commit()
            return "Recruitment Organisation added - id={}".format(organisation.id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """
        Get All Recruitment Organisations
        """
        try:
            organisations = RecruitmentOrganisation.query.all()
            serialized_organisations = [organisation.serialize() for organisation in organisations]
            return jsonify(serialized_organisations)

        except Exception as ex:
            log.error(ex)


class HandleRecruitmentOrganisation(Resource):
    """This class is used to get or edit a specified Recruitment organisation"""

    def get(self, organisation_id):
        """
        Get specific Recruitment organisation
        """
        try:
            organisation_object = RecruitmentOrganisation.query.filter_by(id=organisation_id).first()
            serialized_organisation = organisation_object.serialize()
            return jsonify(serialized_organisation)
        except Exception as ex:
            log.error(ex)
            return ex

    def put(self, organisation_id):
        """
        Update Recruitment organisation
        """
        data = dict(request.get_json())

        try:
            organisation_object = RecruitmentOrganisation.query.filter_by(id=organisation_id)
            if len(data) != 0:
                organisation_object.update(data)
                db.session.commit()
            return "Organisation with ID: {} updated".format(organisation_id)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, organisation_id):
        """ delete Recruitment organisation """
        try:
            organisation_object = RecruitmentOrganisation.query.filter_by(id=organisation_id)
            if organisation_object.first():
                UserRecruitmentOrganisation.query.filter_by(organisation_id=organisation_id).delete()
                organisation_object.delete()
                db.session.commit()
                return "Organisation with ID: {} deleted".format(organisation_id)
            else:
                return "Organisation does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class UserRecruitmentOrganisationObject(Resource):
    """
    This object is used to:

    1) Create a new User - Recruitment Organisation relationship
    """

    def post(self):
        """
        Append new user - Recruitment organisation relationship
        """
        data = request.get_json()

        try:
            user_organisation_obj = UserRecruitmentOrganisation(
                user_id=data['user_id'],
                organisation_id=data['recruitment_organisation_id']
            )

            db.session.add(user_organisation_obj)
            db.session.commit()
            return "User - Recruitment Organisation Object added.", 201

        except Exception as ex:
            log.error(ex)
            return ex, 400


class HandleUserRecruitmentOrganisation(Resource):
    """This class is used to get, delete a  User Recruitment organisation objects related to given organisation"""

    def get(self, organisation_id):
        """
        Get specific user Recruitment organisation relationship with given org id
        """
        try:
            organisation_objects = UserRecruitmentOrganisation.query.filter_by(organisation_id=organisation_id)
            serialized_organisations = [organisation.serialize() for organisation in
                                        organisation_objects]
            return jsonify(serialized_organisations)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, organisation_id):
        """ delete user Recruitment organisation objects related to given org id"""
        try:
            organisation_objects = UserRecruitmentOrganisation.query.filter_by(organisation_id=organisation_id)
            if organisation_objects.first():
                organisation_objects.delete()
                db.session.commit()
                return "UserOrganisation objects related to organisation with id={} deleted".format(organisation_id)
            else:
                return "Organisation does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class HandleRecruitmentUsers(Resource):
    """This class is used to get, delete a  User Recruitment organisation objects related to given user"""

    def get(self, user_id):
        """
        Get specific user Recruitment organisation relationship with given user id
        """
        try:
            objects = UserRecruitmentOrganisation.query.filter_by(user_id=user_id)
            serialized_obj = [obj.serialize() for obj in objects]
            return jsonify(serialized_obj)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, user_id):
        """ delete user Recruitment organisation objects related to given user id"""
        try:
            objects = UserRecruitmentOrganisation.query.filter_by(user_id=user_id)
            if objects.first():
                objects.delete()
                db.session.commit()
                return "UserOrganisation objects related to user with id={} deleted".format(user_id)
            else:
                return "User does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class RecruitmentOrgansiationUserRelationship(Resource):
    """This class is used to get, delete a specific User Recruitment organisation object"""

    def get(self, relation_id):
        """
        Get specific user Recruitment organisation relationship with given id
        """
        try:
            object = UserRecruitmentOrganisation.query.filter_by(id=relation_id).first()
            serialized_obj = object.serialize()
            return jsonify(serialized_obj)
        except Exception as ex:
            log.error(ex)
            return ex

    def delete(self, relation_id):
        """ delete user Recruitment organisation objects related to given id"""
        try:
            object = UserRecruitmentOrganisation.query.filter_by(id=relation_id).first()
            if object:
                object.delete()
                db.session.commit()
                return "UserOrganisation object with id={} deleted".format(relation_id)
            else:
                return "Object does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex

api.add_resource(AcademicOrganisationObject, '/academicorganisation')
api.add_resource(HandleAcademicOrganisation, '/academicorganisation/<organisation_id>')
api.add_resource(UserAcademicOrganisationObject, '/user/academicorganisation')
api.add_resource(HandleUserAcademicOrganisation, '/user/academicorganisation/<organisation_id>')
api.add_resource(HandleAcademicUsers, '/academicorganisation/user/<user_id>')
api.add_resource(AcademicOrgansiationUserRelationship, '/academicorganisation/user/<user_id>')

api.add_resource(RecruitmentOrganisationObject, '/recruitmentorganisation')
api.add_resource(HandleRecruitmentOrganisation, '/recruitmentorganisation/<organisation_id>')
api.add_resource(UserRecruitmentOrganisationObject, '/user/recruitmentorganisation')
api.add_resource(HandleUserRecruitmentOrganisation, '/user/recruitmentorganisation/<organisation_id>')
api.add_resource(HandleRecruitmentUsers, '/recruitmentorganisation/user/<user_id>')
api.add_resource(RecruitmentOrgansiationUserRelationship, '/recruitmentorganisation/user/<user_id>')
