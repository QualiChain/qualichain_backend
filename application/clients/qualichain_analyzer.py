import json

import requests

from application.settings import ANALYZER_HOST, ANALYZER_PORT, ANALYZER_ENDPOINT, JOB_INDEX, JOB_PROPERTIES


class QualiChainAnalyzer(object):
    def __init__(self):
        self.host = ANALYZER_HOST
        self.port = ANALYZER_PORT
        self.ask = "http://{}:{}/{}".format(self.host, self.port, ANALYZER_ENDPOINT)

    def create_job_index(self):
        """This function is used to initialize qc_job index"""
        payload = JOB_PROPERTIES

        payload['index'] = JOB_INDEX
        payload['query'] = 'create_index'

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            url=self.ask,
            data=json.dumps(payload),
            headers=headers
        )
        return response

    # def store_job(self):
