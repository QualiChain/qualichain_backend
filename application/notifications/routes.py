# =================================
#   Notification APIs
# =================================
import logging
import sys

from flask import request
from flask_restful import Resource, Api

from application.database import db
from application.models import Notification
from application.notifications import notification_blueprint

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(notification_blueprint)


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
        try:
            notification = Notification.query.filter_by(id=notification_id).first()
            serialized_notification = notification.serialize()
            return serialized_notification, 200
        except Exception as ex:
            log.error(ex)
            return ex, 404

    def post(self, notification_id):
        try:
            notification = Notification.query.filter_by(id=notification_id).first()

            if notification.readed:
                notification.readed = False
                message = "Notification with ID={} Read status={}".format(notification_id, 'False')
            else:
                notification.readed = True
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
            return "Notification with ID={} removed".format(notification_id), 204
        except Exception as ex:
            log.error(ex)
            return ex, 404


# Notification Routes
api.add_resource(NotificationObject, '/notifications')
api.add_resource(HandleNotification, '/notifications/<notification_id>')