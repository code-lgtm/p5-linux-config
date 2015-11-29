__author__ = 'Kumar_Garg'

from . import main
from flask import render_template
from ..model import Category, Item
from forms import EditForm, AddForm
from flask import abort, redirect, url_for
from flask.ext.login import login_required, current_user
from catalog import db

@main.route('/')
@main.route('/dashboard')
def dashboard():
    editForm = EditForm()
    categories = Category.query.all()
    return render_template('main/dashboard.html', categories=categories, editForm=editForm)

@main.route('/edit/item/<int:id>', methods=['GET', 'POST'])
@login_required
def editItem(id):
    item = Item.query.filter_by(id=id).first()

    if int(current_user.get_id()) != item.owner_id:
        abort(403);

    form = EditForm(id=id, name=item.name, description=item.description)
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data

        db.session.add(item)
        db.session.commit()

        return redirect(url_for('main.dashboard'))

    return render_template('main/editItem.html', form=form)

@main.route('/add/item', methods=['GET', 'POST'])
@login_required
def addItem():
    form = AddForm()

    if form.validate_on_submit():
        print current_user.get_id()
        print form.category.data
        item = Item(name=form.name.data, description=form.description.data,
                    owner_id=int(current_user.get_id()), category_id=int(form.category.data))

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main.dashboard'))

    return render_template('main/addItem.html', form=form)

@main.route('/delete/item/<int:id>', methods=['GET'])
@login_required
def deleteItem(id):
    item = Item.query.filter_by(id=id).first()

    if item is not None:
        if int(current_user.get_id()) != item.owner_id:
            abort(403);
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for('main.dashboard'))