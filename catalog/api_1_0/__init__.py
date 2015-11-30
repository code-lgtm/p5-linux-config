"""
API Blueprint. All API routes needs to be defined in this package
"""

from flask import Blueprint

api = Blueprint('api', __name__)

from . import categories, errors
