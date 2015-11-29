__author__ = 'Kumar_Garg'

from . import api
from ..model import Category, Item
from flask import jsonify


@api.route('/categories/')
def get_categories():
    """ Provides list of categories. User Login is not required to access
    category list

    :return:
    Categories are returned in json in the following format:
    {
        "categories": [
        {
            "id": <id1>,
            "name": <name1>
        },
        {
            "id": <id2>,
            "name": <name2>
        }
    }
    """
    categories = Category.query.all()
    return jsonify({'categories':
                        [cgory.to_json() for cgory in categories]})


@api.route('/category/<int:id>')
def category(id):
    """
    Provide list of items in the specified category. User Login is not required
    to access item list

    :param
    id: unique identifier of the cateory

    :return:
    Items of the specified category in the following format:
    {
        "items": [
        {
          "category": <category 1>,
          "description": <item description>,
          "timestamp": <item creation date>,
          "isOwner": <1 if logged in user is owner, 0 otherwise>,
          "id": 23, <item unique identifier>
          "name": <item name>
        }
        ]
    }
    """
    items = Item.query.filter(Item.category_id == id).all()
    for item in items:
        print item.to_json()
    return jsonify({"items": [item.to_json() for item in items]})
