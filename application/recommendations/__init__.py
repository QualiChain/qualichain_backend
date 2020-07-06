from flask import Blueprint


recommendation_blueprint = Blueprint('recommendations', __name__)


from application.recommendations import routes