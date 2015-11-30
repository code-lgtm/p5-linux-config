"""
Edit Item and Add Item web forms created using Flask-WTF extension
"""

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, HiddenField
from wtforms import TextAreaField, SelectField
from wtforms.validators import Length, DataRequired
from ..model import Category


class EditForm(Form):
    """
    Edit Item form. Id of the field would br hidden.
    Item Name is restricted to 64 characters
    Item Description is restricted to 256
    """
    id = HiddenField('id', validators=[DataRequired(), ])
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 256)])
    submit = SubmitField('Submit')


class AddForm(Form):
    """
    Add Item form.
    Item Name is restricted to 64 characters
    Item Description is restricted to 256 characters
    """
    category = SelectField('Category', coerce=int)
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 256)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        """ Initializes Add Item Form

        :param args:
        :param kwargs:
        :return:
        """
        super(AddForm, self).__init__(*args, **kwargs)
        # Prepopulate  available Categories in category field in web form
        self.category.choices = [(category.id, category.name) for category in
                                 Category.query.order_by(Category.name).all()]
