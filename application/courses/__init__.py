from flask import Blueprint


course_blueprint = Blueprint('courses', __name__)


from application.courses import routes