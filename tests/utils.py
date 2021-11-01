import http.client
from codecs import encode
import json


authentication_endpoint = 'qualichain.herokuapp.com'


def login(username, password):
    response_data = create_request(username, password)
    token, user_id = get_token_and_user_id_from_response(response_data)
    # print(data.decode("utf-8"))
    return token, user_id


def create_request(username, password):
    conn = http.client.HTTPSConnection(authentication_endpoint)
    data_list = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    data_list.append(encode('--' + boundary))
    data_list.append(encode('Content-Disposition: form-data; name=username;'))
    data_list.append(encode('Content-Type: {}'.format('text/plain')))
    data_list.append(encode(''))
    data_list.append(encode(username))
    data_list.append(encode('--' + boundary))
    data_list.append(encode('Content-Disposition: form-data; name=password;'))
    data_list.append(encode('Content-Type: {}'.format('text/plain')))
    data_list.append(encode(''))
    data_list.append(encode(password))
    data_list.append(encode('--' + boundary + '--'))
    data_list.append(encode(''))
    body = b'\r\n'.join(data_list)
    payload = body
    headers = {
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/users/login", payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data


def get_token_and_user_id_from_response(response_data):
    json_data = json.loads(response_data)
    return json_data["response_data"]["token"], json_data["response_data"]["user"]["id"]