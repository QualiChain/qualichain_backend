import logging
import sys
from flask import request

import requests
from flask_restful import Resource, Api
from application.curriculum_recommendations import curriculum_recommendation_blueprint
from application.decorators import only_professors_or_academic_oranisations
import json


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(curriculum_recommendation_blueprint)

CURRICULUM_DESIGNER_ENDPOINT = 'http://qualichain.epu.ntua.gr:8080/curriculum_recommendation'


class CurriculumRecommendation(Resource):
    method_decorators = {'post': [only_professors_or_academic_oranisations]}

    def post(self):
        request_body = request.json
        response = requests.post(CURRICULUM_DESIGNER_ENDPOINT, json=request_body)
        return json.loads(response.content), response.status_code


api.add_resource(CurriculumRecommendation, '/curriculum_design')
