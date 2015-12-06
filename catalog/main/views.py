"""
Provides routes for following:
    1) Dashboard
    2) Edit Item
    3) Add Item
    4) Delete Item
"""

from . import main
from flask import render_template
from ..model import Category, Item
from forms import EditForm, AddForm
from flask import abort, redirect, url_for, request
from flask.ext.login import login_required, current_user
from catalog import db, csrf
import bleach


@main.route('/')
@main.route('/dashboard')
def dashboard():
    """
    View for currently available categories. Rendered view would
    make subsequent api requests at /category/<int:id> where id
    represents unique category id. Edit and Delete options would
    be given to the items for which the logged in user is the
    owner

    :return: Dashboard Page
    """
    categories = Category.query.all()
    return render_template('main/dashboard.html', categories=categories)

@main.route('/edit/item/<int:id>', methods=['GET', 'POST'])
@login_required
def editItem(id):
    """
    Logged in User attempts to edit an item

    :param id: unique identifier of the item
    :return: GET : Renders Edit Item form
             POST: Adds item to database and redirects user
    """
    item = Item.query.filter_by(id=id).first()

    # Abort if logged in user is not the owner of the page
    if int(current_user.get_id()) != item.owner_id:
        abort(403);

    form = EditForm(id=id, name=item.name, description=item.description)
    if form.validate_on_submit():
        item.name = bleach.clean(form.name.data)
        item.description = bleach.clean(form.description.data)

        db.session.add(item)
        db.session.commit()

        return redirect(url_for('main.dashboard'))

    return render_template('main/editItem.html', form=form)

@main.route('/add/item', methods=['GET', 'POST'])
@login_required
def addItem():
    """
    Logged in user attempts to add an item

    :return: GET : Renders Add Item Form
             POST : Inserts added item to database and redirects user
             dashbiard page
    """
    form = AddForm()

    if form.validate_on_submit():
        print current_user.get_id()
        print form.category.data
        item = Item(name=bleach.clean(form.name.data),
                    description=bleach.clean(form.description.data),
                    owner_id=int(current_user.get_id()),
                    category_id=int(form.category.data))

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main.dashboard'))

    return render_template('main/addItem.html', form=form)


@main.route('/delete/item', methods=['POST'])
@login_required
def deleteItem():
    """
    Deletes an item

    :param id: unique identifier of the item to be removed
    :return: 403 : If logged in user is not the owner of the page
             else redirects to dashboard page after deleting the item
    """
    id = request.form['delId']
    item = Item.query.filter_by(id=id).first()

    if item is not None:
        if int(current_user.get_id()) != item.owner_id:
            abort(403);
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for('main.dashboard'))
