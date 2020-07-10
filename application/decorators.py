from functools import wraps

import flask_restful

from application.utils import mock_response_from_inesc


def authenticate_user(func):
    """Decorator that is used for user authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        mock_response = mock_response_from_inesc()
        if mock_response == 200:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper
