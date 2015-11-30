"""
Error Handlers for errors originating while accessing API's
"""
from flask import jsonify
from . import api

@api.errorhandler(400)
def bad_request(message):
    """ This function is called if server perceives a client error such as
    malformed request syntax, invalid request message framing or deceptive
    request routing

    :param message: Message to be returned to the user
    :return: json response containing 400 error code and message
    """
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

@api.errorhandler(401)
def unauthorized(message):
    """ This function is called when user doesn't have necessary credentials
    to access the requested resource

    :param message: Message to be returned to the user
    :return: json response containing 401 error code and message
    """
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response
