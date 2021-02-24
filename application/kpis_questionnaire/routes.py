# =================================
#   KPIs_Questionnaire APIs
# =================================
import logging
import sys

from flask import request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.sql import func
from application.database import db
from application.models import Questionnaire, Kpi, KpiTime
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

    def get(self):
        """
        Get all user reviews
        """
        try:
            results = Questionnaire.query.all()
            serialized_results = [result.serialize() for result in results]
            return jsonify(serialized_results)

        except Exception as ex:
            log.error(ex)


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

    def get(self):
        """
        Get all counter kpis
        """
        try:
            results = Kpi.query.all()
            serialized_results = [result.serialize() for result in results]
            return jsonify(serialized_results)

        except Exception as ex:
            log.error(ex)


class KpiTimeObject(Resource):
    def post(self):
        try:
            data = dict(request.get_json())
            kpi_obj = KpiTime(kpi_name=data['kpi_name'], time=data['time'])
            db.session.add(kpi_obj)
            db.session.commit()
            return 'KpiTimeObject {} with time {} in microseconds added.'.format(data['kpi_name'], data['time']), 201
        except Exception as ex:
            log.error(ex)
            return ex, 400

    def get(self):
        """
        Get average time of specific process
        """

        if request.args.get('kpi_name') is not None:
            kpi_name = request.args.get('kpi_name')
            try:
                kpi_time_obj = KpiTime.query.filter_by(kpi_name=kpi_name)
                if kpi_time_obj.first():
                    kpi_time_avg = db.session.query(func.avg(KpiTime.time).label('average_time')).filter(
                        KpiTime.kpi_name == kpi_name)
                    return 'Average time= {} microseconds'.format(str(int(kpi_time_avg.first().average_time))), 201
                else:
                    return 'There is no KPI with the provided name'
            except Exception as ex:
                log.error(ex)
                return ex
        else:
            return 'KPI name not provided in the request', 404


# KPIs Questionnaire Routes
api.add_resource(QuestionnaireObject, '/questionnaire')
api.add_resource(KpiObject, '/kpi')
api.add_resource(KpiTimeObject, '/kpi_time')
