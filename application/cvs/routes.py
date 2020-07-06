import logging
import sys

from flask import request, jsonify
from flask_restful import Resource, Api

from application.cvs import cv_blueprint
from application.database import db
from application.models import CV

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(cv_blueprint)


class HandleCV(Resource):
    """
    This class is used to create a new CV for user or retrieve the CV of a user
    """

    def post(self, user_id):
        """
        Create a new User
        """
        data = request.get_json()

        try:
            cv = CV(
                user_id=user_id,
                person_URI=data['PersonURI'],
                label=data['Label'],
                target_sector=data['targetSector'],
                expected_salary=data['expectedSalary'],
                description=data['Description'],
                skills=data['Skills'],
                work_history=data['workHistory'],
                education=data['Education']
            )
            db.session.add(cv)
            db.session.commit()
            return "CV added for user={}".format(user_id), 201

        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self, user_id):
        """
        Get the CV of a user
        """
        try:
            cvs = CV.query.filter_by(user_id=user_id)
            serialized_cvs = [cv.serialize() for cv in cvs]
            return jsonify(serialized_cvs)

        except Exception as ex:
            log.error(ex)

    def delete(self, user_id):
        """ delete the CV of a user """
        try:
            cvs = CV.query.filter_by(user_id=user_id)
            if cvs.first():
                cvs.delete()
                db.session.commit()
                return "CV of user with ID={} removed".format(user_id)
            else:
                return "CV does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex, 404


# CVs routes
api.add_resource(HandleCV, '/CV/<user_id>')
