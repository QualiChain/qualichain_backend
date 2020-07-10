from functools import wraps

import flask_restful
from flask import request

from application.utils import mock_response_from_inesc


def only_profile_owner(func):
    """Decorator that is used for user authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        request_token = request.headers.get("Authorization", None)
        user_id = request.view_args.get('user_id', None)

        if request_token is None or user_id is None:
            flask_restful.abort(401)

        mock_response = mock_response_from_inesc(request_token, user_id)
        if mock_response:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper
