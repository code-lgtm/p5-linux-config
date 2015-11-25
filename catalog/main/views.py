__author__ = 'Kumar_Garg'

from . import main
from flask import render_template
from ..model import Category, Item

@main.route('/')
def dashboard():
    categories = Category.query.all()
    return render_template('main/dashboard.html', categories=categories)


