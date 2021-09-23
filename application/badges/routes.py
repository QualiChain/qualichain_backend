# =================================
#   SmartBadge APIs
# =================================
import logging
import sys

from flask import request
from flask_restful import Resource, Api
from sqlalchemy import func

from application.badges import badge_blueprint
from application.database import db
from application.models import SmartBadge, UserBadgeRelation, BadgeCourseRelation, User, Notification
from application.utils import kpi_measurement
from application.decorators import only_professors_or_academic_oranisations, only_authenticated, only_admins

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(badge_blueprint)


class SmartBadgeObject(Resource):
    """This class is used to Create a new Smart Badge and retrieve all stored Smart Badges"""

    method_decorators = {'post': [only_authenticated], 'get': [only_authenticated]}

    def post(self):
        """Create a new Smart Badge"""
        data = request.get_json()
        print(data)

        try:
            oubadge = data['oubadge']
            issuer = oubadge['issuer']
            smart_badge = SmartBadge(
                name=oubadge['name'],
                issuer=issuer['name'],
                description=oubadge['description'],
                type=data['type'],
                oubadge=data['oubadge']
            )
            db.session.add(smart_badge)
            db.session.commit()
            kpi_measurement('create_smart_badge')
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

    method_decorators = {'delete': [only_admins], 'get': [only_authenticated]}

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
        course_id = request.args.get('course_id', None)
        badge_id = request.args.get('badge_id', None)

        if course_id and badge_id:
            try:
                course_badges = BadgeCourseRelation.query.filter_by(course_id=course_id, badge_id=badge_id)

                if course_badges:
                    course_badges.delete()
                    db.session.commit()
                    return "Course - Badge Relation deleted", 200
                else:
                    return "Course - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "Bad Request", 400

class ListOfAwardableBadges(Resource):
    """This class is used to retrieve a list of badges a user is allowed to award to another user"""
    def get(self):
        """Get User's Badges with aggregated awardings per badge"""
        user_id = request.args.get('user_id', None)
        awarder_id = request.args.get('awarder_id', None)

        if user_id and awarder_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, awarded_by_id=awarder_id).all()
                badge_list = (badge.badge_id for badge in user_badges)
                badges = SmartBadge.query.filter(SmartBadge.id.notin_(badge_list)).all()
                serialized_user_badge = [badge.serialize() for badge in badges]
                return serialized_user_badge, 200
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "User-id and awarder-id needs to be provided- Bad request", 400

class ListOfBadgesAggregated(Resource):
    """This class is used to handle User - Badge Relations by returning lists of badges along with counters"""

    def get(self):
        """Get User's Badges with aggregated awardings per badge"""
        user_id = request.args.get('user_id', None)

        if user_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id).with_entities(
                    UserBadgeRelation.badge_id, func.count(UserBadgeRelation.badge_id)).group_by(UserBadgeRelation.badge_id).all()

                badge_list = []
                for badge in user_badges:
                    sb = SmartBadge.query.filter_by(id=badge[0]).first()
                    badge_dict = {"badge_details": sb.serialize(), "count": badge[1]}
                    badge_list.append(badge_dict)

                return badge_list, 200
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "User-id and Smart badge-id needs to be provided- Bad request", 400


class DetailsOfBadgeAwarding(Resource):
    """This class is used to gather details about the awardings of a specific badge"""

    def get(self):
        """Get User's Badge with all details regarding its awardings"""
        user_id = request.args.get('user_id', None)
        badge_id = request.args.get('badge_id', None)
        if badge_id and user_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id).with_entities(
                    UserBadgeRelation.awarded_by_role, func.count(UserBadgeRelation.awarded_by_role)).group_by(UserBadgeRelation.awarded_by_role).all()

                badge_info = {}
                sb = SmartBadge.query.filter_by(id=badge_id).first()
                badge_info['badge_info'] = sb.serialize()
                badge_info['awarded_by'] = {}
                for el in user_badges:
                    badge_info['awarded_by'][el[0]] = el[1]

                return badge_info, 200

            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "User-id and Smart badge-id needs to be provided- Bad request", 400


class NewUserBadgeAssignment(Resource):
    """This class is used to handle User - Badge Relation"""

    # method_decorators = {'post': [only_authenticated], 'get': [only_authenticated], 'delete': [only_admins]}

    def post(self):
        """Create User - Badge Relation"""
        data = request.get_json()
        try:
            if "ou_metadata" in data:
                ou_metadata = data['ou_metadata']
            else:
                ou_metadata = None
            relation = UserBadgeRelation(
                badge_id=data['badge_id'],
                user_id=data['user_id'],
                oubadge_user=data['oubadge_user'],
                ou_metadata=ou_metadata
            )
            if 'awarded_by_id' in data:
                relation.awarded_by_id = data['awarded_by_id']
            if 'awarded_by_role' in data:
                relation.awarded_by_role = data['awarded_by_role']

            db.session.add(relation)
            smart_badge = SmartBadge.query.filter_by(id=data['badge_id'])[0]
            message = "You just received a smart badge '{}'.".format(smart_badge.name)

            new_badge_notification = Notification(user_id=data['user_id'], message=message)
            db.session.add(new_badge_notification)
            db.session.commit()
            kpi_measurement('issue_badge_to_user')
            return "relation between UserID={} and BadgeID={} created".format(data['user_id'], data['badge_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get User - (Specific) Badge Relations - All awardings of a selected badge"""
        user_id = request.args.get('user_id', None)
        badge_id = request.args.get('badge_id', None)

        if badge_id and user_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id)

                if user_badges:
                    serialized_user_badge = [relation.serialize() for relation in user_badges]
                    return serialized_user_badge, 200
                else:
                    return "User - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "User-id and Smart badge-id needs to be provided- Bad request", 400


    def delete(self):
        """Delete User - Badge Relation"""

        user_id = request.args.get('user_id', None)
        badge_id = request.args.get('badge_id', None)
        awarder_id = request.args.get('awarder_id', None)

        if user_id and badge_id and awarder_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id,
                                                                awarded_by_id=awarder_id)
                print(user_badges)

                if user_badges:
                    user_badges.delete()
                    db.session.commit()
                    return "User - Badge Relation deleted", 200
                else:
                    return "User - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        elif user_id and badge_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id)
                print(user_badges)

                if user_badges:
                    user_badges.delete()
                    db.session.commit()
                    return "User - Badge Relations deleted", 200
                else:
                    return "User - Badge Relations do not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400

        else:
            return "Bad Request", 400


# old implementation of badges
class UserBadgeAssignment(Resource):
    """This class is used to handle User - Badge Relation"""

    method_decorators = {'post': [only_authenticated], 'get': [only_authenticated]}

    def post(self):
        """Create User - Badge Relation"""
        data = request.get_json()

        try:
            if "ou_metadata" in data:
                ou_metadata = data['ou_metadata']
            else:
                ou_metadata = None
            relation = UserBadgeRelation(
                badge_id=data['badge_id'],
                user_id=data['user_id'],
                oubadge_user=data['oubadge_user'],
                ou_metadata=ou_metadata
            )

            db.session.add(relation)
            smart_badge = SmartBadge.query.filter_by(id=data['badge_id'])[0]
            message = "You just received a smart badge '{}'.".format(smart_badge.name)

            new_badge_notification = Notification(user_id=data['user_id'], message=message)
            db.session.add(new_badge_notification)
            db.session.commit()
            kpi_measurement('issue_badge_to_user')
            return "relation between UserID={} and BadgeID={} created".format(data['user_id'], data['badge_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """Get User - (Specific) Badge Relation"""
        user_id = request.args.get('userid', None)
        badge_id = request.args.get('badgeid', None)

        if badge_id:
            if user_id:
                try:
                    user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id)

                    if user_badges:
                        serialized_user_badge = [relation.serialize() for relation in user_badges]
                        return serialized_user_badge[0], 200
                    else:
                        return "User - Badge Relation does not exist", 404
                except Exception as ex:
                    log.error(ex)
                    return ex, 400
            else:
                return "Bad Request", 400
        else:
            try:
                if user_id:
                    user_badges = UserBadgeRelation.query.filter_by(user_id=user_id)
                else:
                    user_badges = UserBadgeRelation.query.all()

                serialized_relations = [relation.serialize() for relation in user_badges]
                return serialized_relations, 200
            except Exception as ex:
                log.error(ex)
                return ex, 400

    def delete(self):
        """Delete User - Badge Relation"""

        user_id = request.args.get('user_id', None)
        badge_id = request.args.get('badge_id', None)

        if user_id and badge_id:
            try:
                user_badges = UserBadgeRelation.query.filter_by(user_id=user_id, badge_id=badge_id)
                print(user_badges)

                if user_badges:
                    user_badges.delete()
                    db.session.commit()
                    return "User - Badge Relation deleted", 200
                else:
                    return "User - Badge Relation does not exist", 404
            except Exception as ex:
                log.error(ex)
                return ex, 400
        else:
            return "Bad Request", 400


class GetBadgeViaEmail(Resource):
    """This object is used for retrieving a Badge via user's email"""
    method_decorators = {'post': [only_authenticated], 'get': [only_authenticated]}

    def post(self):
        """Retrieve user's smart badges"""
        data = request.get_json()
        email = data['email']
        if_user_exists = User.query.filter_by(email=email).scalar()
        if if_user_exists:
            user_smart_badges_obj = SmartBadge.query.filter_by(
                issuer=email
            )
            user_smart_badges = [badge.serialize() for badge in user_smart_badges_obj]
            return user_smart_badges, 201
        else:
            return "The user with email: {} does not exists".format(email), 400


# Smart Badges Routes
api.add_resource(SmartBadgeObject, '/badges')
api.add_resource(HandleSmartBadge, '/badges/<badge_id>')
api.add_resource(CourseBadgeAssignment, '/course/badges')
api.add_resource(UserBadgeAssignment, '/user/badges')
api.add_resource(NewUserBadgeAssignment, '/user/awards')
api.add_resource(ListOfBadgesAggregated, '/aggregate/awards')
api.add_resource(ListOfAwardableBadges, '/awardable/badges')
api.add_resource(DetailsOfBadgeAwarding, '/details/awards')
api.add_resource(GetBadgeViaEmail, '/get/badge/by/email')
