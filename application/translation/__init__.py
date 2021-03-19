from flask import Blueprint


translation_blueprint = Blueprint('translation', __name__)


from application.translation import routes