from flask import Blueprint

skill_blueprint = Blueprint('skills', __name__)

from application.skills import routes
