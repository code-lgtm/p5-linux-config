__author__ = 'Kumar_Garg'

from . import api
from ..model import Category, Item
from flask import jsonify

@api.route('/categories/')
def get_categories():
    categories  = Category.query.all()
    return jsonify({'categories' :
                        [category.to_json()  for category in categories ]})
