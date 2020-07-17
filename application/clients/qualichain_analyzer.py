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

    def store_job(self, **kwargs):
        """This function is used to store Job data to Analyzer"""
        payload = kwargs

        payload['index'] = JOB_INDEX
        payload['query'] = 'create_document'

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            url=self.ask,
            data=json.dumps(payload),
            headers=headers
        )
        return response

    def search_job(self, **kwargs):
        """This function is used to search stored jobs in QualiChain"""
        search_params = kwargs
        headers = {
            'Content-Type': 'application/json'
        }

        search_body = {
            "query": "bool_query",
            "min_score": 0.0,
            "index": JOB_INDEX,
            "must": [
                {
                    "match": {
                        param: search_params[param]
                    }
                } for param in search_params.keys()]
        }

        response = requests.post(
            url=self.ask,
            headers=headers,
            data=json.dumps(search_body)
        )
        return response

    def delete_job(self, job_id):
        """This function is used to remove a stored job"""

        headers = {
            'Content-Type': 'application/json'
        }

        body = {
            "query": "delete_document",
            "index": JOB_INDEX,
            "id": job_id
        }
        response = requests.post(
            url=self.ask,
            headers=headers,
            data=json.dumps(body)
        )
        return response
