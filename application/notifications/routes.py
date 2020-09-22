# =================================
#   Notification APIs
# =================================
import logging
import sys

from flask import request, jsonify
from flask_restful import Resource, Api

from application.database import db
from application.models import Notification, UserNotificationPreference
from application.notifications import notification_blueprint

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(notification_blueprint)


class UserNotificationPreferenceObject(Resource):
    def post(self):
        try:
            data = dict(request.get_json())

            preference_obj = UserNotificationPreference.query.filter_by(user_id=data['user_id'])
            user_preference_exists = preference_obj.scalar()

            if not user_preference_exists:
                preference_obj = UserNotificationPreference(user_id=data['user_id'],
                                                            locations=data['locations'],
                                                            specializations=data['specializations']
                                                            )
                db.session.add(preference_obj)
                db.session.commit()
                return 'Notification preferences added for UserID={}'.format(data['user_id']), 201
            else:

                preference_obj.specialisations = data['specializations']
                preference_obj.locations = data['locations']

                db.session.commit()
                return 'Notification preferences edited for UserID={}'.format(data['user_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        user_id = request.args.get('user_id', None)
        try:
            preference_obj = UserNotificationPreference.query.filter_by(user_id=user_id)
            pref_exists = preference_obj.scalar()
            if pref_exists:
                serialized_preference = preference_obj[0].serialize()
                return serialized_preference, 200
            else:
                return {}
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self):
        preference_id = request.args.get('preference_id', None)
        try:
            not_preference = UserNotificationPreference.query.filter_by(id=preference_id)
            not_preference_exists = not_preference.scalar()
            if not_preference_exists:
                not_preference.delete()
                db.session.commit()
                return "Preference with ID={} removed".format(preference_id)
            else:
                return "There is no such preference id"
        except Exception as ex:
            log.error(ex)
            return ex, 404


class NotificationObject(Resource):
    def post(self):
        data = request.get_json()

        try:
            notification_obj = Notification(
                message=data['message'],
                user_id=data['user_id']
            )

            db.session.add(notification_obj)
            db.session.commit()
            return 'Notification added for UserID={}'.format(data['user_id']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        user_id = request.args.get('userid', None)

        try:
            if user_id:
                notifications = Notification.query.filter_by(user_id=user_id)
            else:
                notifications = Notification.query.all()

            serialized_notifications = [notification.serialize() for notification in notifications]
            return serialized_notifications, 200
        except Exception as ex:
            log.error(ex)
            return ex, 404


class HandleNotification(Resource):
    def get(self, notification_id):
        notification_obj = Notification.query.filter_by(id=notification_id)
        notification_exists = notification_obj.scalar()
        if notification_exists:
            notification = Notification.query.filter_by(id=notification_id).first()
            serialized_notification = notification.serialize()
            return serialized_notification
        else:
            return {"msg": "Notification ID={} does not exists".format(notification_id)}, 404

    def post(self, notification_id):
        try:
            notification = Notification.query.filter_by(id=notification_id).first()

            if notification.read:
                notification.read = False
                message = "Notification with ID={} Read status={}".format(notification_id, 'False')
            else:
                notification.read = True
                message = "Notification with ID={} Read status={}".format(notification_id, 'True')

            db.session.commit()
            return message, 201
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def delete(self, notification_id):
        try:
            notification = Notification.query.filter_by(id=notification_id)
            notification.delete()
            db.session.commit()
            return {"msg": "Notification with ID={} removed".format(notification_id)}, 204
        except Exception as ex:
            log.error(ex)
            return ex, 404


# Notification Routes
api.add_resource(UserNotificationPreferenceObject, '/set/notification/preferences')
api.add_resource(NotificationObject, '/notifications')
api.add_resource(HandleNotification, '/notifications/<notification_id>')
