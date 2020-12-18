from flask import Blueprint


kpis_questionnaire_blueprint = Blueprint('kpis_questionnaire', __name__)


from application.kpis_questionnaire import routes