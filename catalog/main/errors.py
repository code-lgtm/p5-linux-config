__author__ = 'Kumar_Garg'

from . import main

@main.app_errorhandler(403)
def authorization_error(e):
    print e
    return 'Authorization Error', 403

@main.app_errorhandler(404)
def page_not_found(e):
    return 'Not Found', 404

@main.app_errorhandler(500)
def internal_server_error(e):
    print e
    return 'Internal Server Error', 500
