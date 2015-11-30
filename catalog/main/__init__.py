"""
Package consists of the key functional areas of the application
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..model import Permission

@main.app_context_processor
def inject_permissions():
    """
    Context processor to make permissions available to templates

    :return:
    Dictionary containing Permission class and its bit constants
    """
    return dict(Permission = Permission)


