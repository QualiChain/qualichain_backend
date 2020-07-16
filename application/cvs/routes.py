import logging
import sys

from flask import request, jsonify
from flask_restful import Resource, Api

from application.cvs import cv_blueprint
from application.database import db
from application.models import CV, CVSkill

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
        Create a new CV
        """
        data = request.get_json()
        cvs = CV.query.filter_by(user_id=user_id).scalar()
        if cvs is None:
            try:
                cv = CV(
                    user_id=user_id,
                    target_sector=data['targetSector'],
                    description=data['Description'],
                    work_history=data['workHistory'],
                    education=data['Education']
                )
                db.session.add(cv)
                db.session.commit()

                skills_in_data = 'skills' in data.keys()
                if skills_in_data:
                    for skill in data['skills']:
                        new_skill = CVSkill(skill_id=skill['id'], cv_id=cv.id)
                        db.session.add(new_skill)
                    db.session.commit()
                    return "CV added. course={}".format(cv.id), 201
                else:
                    return "Skills required for submitted course.", 400

            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "CV already exists", 201

    def get(self, user_id):
        """
        Get the CV of a user
        """
        try:
            cvs = CV.query.filter_by(user_id=user_id)
            print(cvs)
            serialized_cvs = [cv.serialize() for cv in cvs]
            return jsonify(serialized_cvs)

        except Exception as ex:
            log.error(ex)

    def delete(self, user_id):
        """ delete the CV of a user """
        try:
            cvs = CV.query.filter_by(user_id=user_id)
            if cvs.first():
                CVSkill.query.filter_by(cv_id=cvs.first().id).delete()
                cvs.delete()
                db.session.commit()
                return "CV of user with ID={} removed".format(user_id)
            else:
                return "CV does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex, 404


class SkillsToCV(Resource):
    """This interface appends skills to CV"""

    def post(self, cv_id):
        try:
            data = request.get_json()
            skill_id = data['skill_id']

            skill_cv = CVSkill(
                cv_id=cv_id,
                skill_id=skill_id
            )
            db.session.add(skill_cv)
            db.session.commit()
        except Exception as ex:
            log.error(ex)
            return ex

    def get(self, cv_id):
        """
        Get all skills from the given cv
        """
        try:
            cv_skills = CVSkill.query.filter_by(
                cv_id=cv_id
            )
            results = [skill_cv_rel.serialize() for skill_cv_rel in cv_skills]
            return results, 200
        except Exception as ex:
            log.error(ex)
            return ex


# CVs routes
api.add_resource(HandleCV, '/CV/<user_id>')
api.add_resource(SkillsToCV, '/SkillsToCV/<cv_id>')
