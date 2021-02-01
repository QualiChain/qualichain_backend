from flask import Blueprint


course_recommendation_blueprint = Blueprint('course_recommendations', __name__)


from application.course_recommendations import routes