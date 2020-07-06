from flask import Blueprint


mediator_blueprint = Blueprint('mediator', __name__)


from application.mediator import routes