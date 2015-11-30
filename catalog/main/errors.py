"""
Error Handlers for errors originating in the main functional
aareas of application
"""

from . import main
from flask import jsonify


@main.app_errorhandler(401)
def authorization_error(message):
    """ This function is called when user doesn't have necessary credentials
    to access the requested resource

    :param message: Message to be returned to the user
    :return: json response containing 401 error code and message
    """
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@main.app_errorhandler(404)
def page_not_found(message):
    """
    This function is called if the requested resource could not be found

    :param message: Message containing error details
    :return: json response containing 404 error code and appropriate error message
    """
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 404
    return response


@main.app_errorhandler(500)
def internal_server_error(message):
    """
    This function is called when an unexpected condition was encountered

    :param message: Message containing error details
    :return: json response containing 500 error code and appropriate error message
    """
    response = jsonify({'error': 'Internal Server Error', 'message': message})
    response.status_code = 500
    return response
