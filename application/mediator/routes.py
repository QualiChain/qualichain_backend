from flask import request, jsonify

from application import producer
from application.clients.fuseki_client import FusekiClient
from application.mediator import mediator_blueprint
from application.settings import IAM_API_KEYS, IAM_PASSWORD


@mediator_blueprint.route('/retrieve_data', methods=['POST'])
def retrieve_saro_data():
    '''
    This api call executes a query and retrieves data from a knowledge graph.
    Post body(json):
    {"query": "String SparQL query to be executed"}
    :return: Returns the results of the query in JSON format.
    '''

    request_data = request.get_json()
    if request_data is not None:
        query = request_data['query']
        fuseki_client = FusekiClient()
        response = fuseki_client.query_fuseki_client(query)
        if response.status_code == 200:
            description = 'Query Completed'
            results = response.json()
            status = response.status_code
        else:
            description = 'Incorrect Query'
            results = {}
            status = response.status_code
    else:
        description = 'Incorrect Request'
        results = {}
        status = '500'

    results = {'status': status, 'results': results, 'description': description}

    return jsonify(results)


@mediator_blueprint.route('/submit_data', methods=['POST'])
def submit_saro_data():
    '''
    This api call submits data to Dobie in order to store the result in the knowledge graph.
    Post body(json):
    {"text": "The text that will be analysed in Dobie}
    '''

    request_data = request.get_json()
    if request_data is not None:
        text = request_data['text']
        producer.add_to_queue(text)
        description = 'Submission Completed'
    else:
        description = 'Incorrect Request'
    results = {'description': description}
    return jsonify(results)


@mediator_blueprint.route('/api_key', methods=['POST'])
def get_api_key():
    """This interface is used to retrieve an API key"""
    request_data = request.get_json()
    domain = request_data['domain']
    application = request_data['application']
    password = request_data['password']

    if domain in IAM_API_KEYS.keys() and application == 'IAM_QC' and password == IAM_PASSWORD:
        api_key = IAM_API_KEYS[domain]
        data_to_return_back = {'api_key': api_key}
        return data_to_return_back, 201
    else:
        return {'msg': 'Permission Denied'}, 403
