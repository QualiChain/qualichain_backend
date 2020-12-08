import logging
import sys
from flask import request

import requests
from flask_restful import Resource, Api
from application.course_recommendations import course_recommendation_blueprint
from application.decorators import only_lifelong_learner
import json


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(course_recommendation_blueprint)

COURSE_REC_ENDPOINT = 'http://qualichain.epu.ntua.gr:7000/recommend'


class SkillCourseRecommendation(Resource):
    method_decorators = {'post': [only_lifelong_learner]}

    def post(self):
        request_body = request.json
        response = requests.post(COURSE_REC_ENDPOINT, json=request_body)
        return json.loads(response.content), response.status_code


api.add_resource(SkillCourseRecommendation, '/recommend')
