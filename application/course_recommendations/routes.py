import logging
import sys
from flask import request

import requests
from flask_restful import Resource, Api
from application.course_recommendations import course_recommendation_blueprint
from application.decorators import only_authenticated
import json
from datetime import datetime
from application.utils import kpi_measurement, kpi_time_measurement



logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(course_recommendation_blueprint)

COURSE_REC_ENDPOINT = 'http://qualichain.epu.ntua.gr:7000/recommend'


class SkillCourseRecommendation(Resource):
    method_decorators = {'post': [only_authenticated]}

    def post(self):
        request_body = request.json
        s_time = datetime.now()
        response = requests.post(COURSE_REC_ENDPOINT, json=request_body)
        kpi_measurement('course_recommendation')
        e_time = datetime.now()
        execution_time = (e_time - s_time).microseconds
        kpi_time_measurement('course_recommendation', execution_time)
        return json.loads(response.content), response.status_code


api.add_resource(SkillCourseRecommendation, '/recommend')
