"""
Authentication Blueprint. All authentication and authorization workflows
needs to be defined in this package
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views, errors
