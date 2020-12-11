# =================================
#   SmartBadge APIs
# =================================
import logging
import sys

from flask import request
from flask_restful import Resource, Api

from application.badges import badge_blueprint
from application.database import db
from application.models import SmartBadge, UserBadgeRelation, BadgeCourseRelation

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(badge_blueprint)


class SmartBadgeObject(Resource):
    """This class is used to Create a new Smart Badge and retrieve all stored Smart Badges"""

    def post(self):
        """Create a new Smart Badge"""
        data = request.get_json()

        try:
            smart_badge = SmartBadge(
                name=data['name'],
                issuer=data['issuer'],
                description=data['description'],
                type=data['type']
            )
            db.session.add(smart_badge)
            db.session.commit()
            return "smart badge with ID={} created".format(smart_badge.id), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get all stored smart badges"""
        try:
            smart_badges = SmartBadge.query.all()
            serialized_badges = [badge.serialize() for badge in smart_badges]
            return serialized_badges, 200
        except Exception as ex:
            log.error(ex)
            return ex


class HandleSmartBadge(Resource):
    """This object is used to handle a specific smart badge"""

    def get(self, badge_id):
        try:
            smart_badge = SmartBadge.query.filter_by(id=badge_id).first()
            serialized_badge = smart_badge.serialize()
            return serialized_badge, 200
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self, badge_id):
        """ delete a specific smart badge """
        try:
            smart_badge = SmartBadge.query.filter_by(id=badge_id)
            if smart_badge.first():
                UserBadgeRelation.query.filter_by(badge_id=badge_id).delete()
                BadgeCourseRelation.query.filter_by(badge_id=badge_id).delete()
                smart_badge.delete()
                db.session.commit()
                return "Smart badge with ID={} deleted".format(badge_id)
            else:
                return "Smart badge with ID={} does not exist".format(badge_id), 404
        except Exception as ex:
            log.error(ex)
            return ex, 404


class CourseBadgeAssignment(Resource):
    """This class is used to handle Course - Badge Relation"""

    def post(self):
        """Create Course - Badge Relation"""
        data = request.get_json()

        try:
            relation = BadgeCourseRelation(
                course_id=data['course_id'],
                badge_id=data['badge_id']
            )

            db.session.add(relation)
            db.session.commit()
            return "relation between CourseID={} and BadgeID={} created".format(data['course_id'],
                                                                                data['badge_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get Course - Badge Relation"""
        course_id = request.args.get('courseid', None)

        try:
            if course_id:

                course_badges = BadgeCourseRelation.query.filter_by(course_id=course_id)
            else:
                course_badges = BadgeCourseRelation.query.all()

            serialized_relations = [relation.serialize() for relation in course_badges]
            return serialized_relations, 200

        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self):
        """Delete Course - Badge Relation"""
        course_id = request.args.get('courseid', None)
        badge_id = request.args.get('badgeid', None)

        if course_id and badge_id:
            try:
                course_badges = BadgeCourseRelation.query.filter_by(course_id=course_id, badge_id=badge_id)

                if course_badges:
                    course_badges.delete()
                    db.session.commit()
                else:
                    return "Course - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "Bad Request", 400


class UserBadgeAssignment(Resource):
    """This class is used to handle User - Badge Relation"""

    def post(self):
        """Create User - Badge Relation"""
        data = request.get_json()

        try:
            relation = UserBadgeRelation(
                badge_id=data['badge_id'],
                user_id=data['user_id']
            )

            db.session.add(relation)
            db.session.commit()
            return "relation between UserID={} and BadgeID={} created".format(data['user_id'], data['badge_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get User - Badge Relation"""
        user_id = request.args.get('userid', None)

        try:
            if user_id:

                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id)
            else:
                user_badges = UserBadgeRelation.query.all()

            serialized_relations = [relation.serialize() for relation in user_badges]
            return serialized_relations, 200

        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self):
        """Delete User - Badge Relation"""

        user_id = request.args.get('userid', None)
        badge_id = request.args.get('badgeid', None)

        if user_id and badge_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id)
                print(user_badges)

                if user_badges:
                    user_badges.delete()
                    db.session.commit()
                else:
                    return "User - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "Bad Request", 400


# Smart Badges Routes
api.add_resource(SmartBadgeObject, '/badges')
api.add_resource(HandleSmartBadge, '/badges/<badge_id>')
api.add_resource(CourseBadgeAssignment, '/course/badges')
api.add_resource(UserBadgeAssignment, '/user/badges')