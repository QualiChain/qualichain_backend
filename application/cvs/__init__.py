from flask import Blueprint


cv_blueprint = Blueprint('cvs', __name__)


from application.cvs import routes