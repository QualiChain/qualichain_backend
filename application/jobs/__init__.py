from flask import Blueprint


job_blueprint = Blueprint('jobs', __name__)


from application.jobs import routes