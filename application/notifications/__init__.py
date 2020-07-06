from flask import Blueprint


notification_blueprint = Blueprint('notifications', __name__)


from application.notifications import routes