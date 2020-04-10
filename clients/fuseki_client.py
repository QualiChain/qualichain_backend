import urllib.parse

import requests

from settings import FUSEKI_CLIENT_HOST, FUSEKI_CLIENT_PORT, FUSEKI_CLIENT_DATASET


class FusekiClient(object):
    def __init__(self):
        self.FUSEKI_CLIENT_BASE_URL = "http://{}:{}".format(
            FUSEKI_CLIENT_HOST,
            FUSEKI_CLIENT_PORT
        )

    def query_fuseki_client(self, sparql_query):
        """
        This function is used to generate queries against SARO dataset

        :param sparql_query: provided SPARQL query
        :return: response from Fuseki CLIENT
        """
        query_endpoint = urllib.parse.urljoin(
            self.FUSEKI_CLIENT_BASE_URL,
            FUSEKI_CLIENT_DATASET
        )

        params = {'query': sparql_query}
        response = requests.get(
            url=query_endpoint,
            params=params
        )
        return response
