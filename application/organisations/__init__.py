from flask import Blueprint


organisation_blueprint = Blueprint('organisations', __name__)


from application.organisations import routes