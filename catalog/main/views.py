__author__ = 'Kumar_Garg'

from . import main
from flask import render_template
from ..model import Category

@main.route('/')
def dashboard():
    categories = Category.query.all()
    print categories
    return render_template('main/dashboard.html', categories=categories)

