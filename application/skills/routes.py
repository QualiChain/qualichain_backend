import logging
import sys

from flask import request, jsonify
from flask_restful import Resource, Api

from application.database import db
from application.models import Skill, UserSkillRecommendation
from application.skills import skill_blueprint

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(skill_blueprint)


class SkillObject(Resource):
    """This object is used to create new skills and return all stored skills"""

    def post(self):
        """Create new skill"""
        data = request.get_json()

        try:
            skill = Skill(
                name=data['name'],
                alternative_labels=data['alternative_labels'],
                description=data['description'],
                hard_skill=data['hard_skill']
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
            return jsonify(serialized_skills)
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

    def delete(self, skill_id):
        """ delete skill """
        try:
            skill_obj = Skill.query.filter_by(id=skill_id)
            if skill_obj.first():
                UserSkillRecommendation.query.filter_by(skill_id=skill_id).delete()
                skill_obj.delete()
                db.session.commit()
                return "Skill with ID: {} deleted".format(skill_id)
            else:
                return "Skill does not exist", 404
        except Exception as ex:
            log.error(ex)
            return ex


class SearchSkill(Resource):
    """Class that is used to search stored skills"""

    def post(self):
        try:
            pattern = request.get_json()['pattern']
            search_pattern = "%{}%".format(pattern)

            skills = Skill.query.filter(Skill.name.like(search_pattern)).all()
            serialized_skills = [skill.serialize() for skill in skills]
            return jsonify(serialized_skills)
        except Exception as ex:
            log.error(ex)
            return ex


# Skill Routes
api.add_resource(SkillObject, '/skills')
api.add_resource(HandleSkill, '/skills/<skill_id>')

api.add_resource(SearchSkill, '/search/skill')