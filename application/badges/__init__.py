from flask import Blueprint


badge_blueprint = Blueprint('badges', __name__)


from application.badges import routes