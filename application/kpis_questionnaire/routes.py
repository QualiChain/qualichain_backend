# =================================
#   KPIs_Questionnaire APIs
# =================================
import logging
import sys

from flask import request
from flask_restful import Resource, Api

from application.database import db
from application.models import Questionnaire, Kpi
from application.kpis_questionnaire import kpis_questionnaire_blueprint

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(kpis_questionnaire_blueprint)


class QuestionnaireObject(Resource):
    def post(self):
        try:
            data = dict(request.get_json())
            satisfaction_level = data['satisfaction_level']
            feedback = data['feedback']

            questionnaire_obj = Questionnaire(satisfaction_level=satisfaction_level, feedback=feedback)
            db.session.add(questionnaire_obj)
            db.session.commit()
            return 'Questionnaire answer added', 201

        except Exception as ex:
            log.error(ex)
            return ex, 400


class KpiObject(Resource):
    def post(self):
        try:
            data = dict(request.get_json())

            kpi_obj = Kpi.query.filter_by(kpi_name=data['kpi_name'])
            kpi_obj_exists = kpi_obj.scalar()

            if not kpi_obj_exists:
                kpi_obj = Kpi(kpi_name=data['kpi_name'], count=1)
                db.session.add(kpi_obj)
                db.session.commit()
                return 'KpiObject added with name={}'.format(data['kpi_name']), 201
            else:
                kpi_obj[0].count = kpi_obj[0].count + 1
                db.session.commit()
                return 'KpiObject: {} updated'.format(data['kpi_name']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400


# KPIs Questionnaire Routes
api.add_resource(QuestionnaireObject, '/questionnaire')
api.add_resource(KpiObject, '/kpi')

