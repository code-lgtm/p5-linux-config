"""
Decorators to be used by the application need be defined in this file
"""

from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .model import Permission


def permission_required(permission):
    """ If decorated on a function, logged in user needs to have the
    necessary privileges to perform the required operation

    :param permission: Permission to be applied
    :return: if permissible function to be applied
             abort otherwise
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """
    If applied, needs administrator privileges to perform function f

    :param f: function to be performed
    :return: function f if logged in user have administrator provileges
             abort otherwise
    """
    return permission_required(Permission.ADMINISTER)(f)
