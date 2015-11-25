from flask import render_template
from . import auth

@auth.app_errorhandler(404)
def page_not_found(e):
    return 'Not Found', 404

@auth.app_errorhandler(500)
def internal_server_error(e):
    print e
    return 'Internal Server Error', 500
