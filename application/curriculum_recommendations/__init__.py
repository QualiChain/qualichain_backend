from flask import Blueprint


curriculum_recommendation_blueprint = Blueprint('curriculum_recommendations', __name__)


from application.curriculum_recommendations import routes