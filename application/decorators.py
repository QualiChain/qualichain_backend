from functools import wraps

import flask_restful
from flask import request

from application.utils import mock_response_from_inesc, check_if_profile_owner
from application.models import User

def only_profile_owner(func):
    """Decorator that is used for user authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id, mock_user_obj, mock_user_roles = check_if_profile_owner(*args, **kwargs)
        print(user_id, mock_user_obj, mock_user_roles)

        if mock_user_obj:
            return func(*args, **kwargs)
        else:
            flask_restful.abort(401)

    return wrapper
