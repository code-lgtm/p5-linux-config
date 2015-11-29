__author__ = 'Kumar_Garg'

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired
from ..model import Category

class EditForm(Form):
    id = HiddenField('id', validators=[DataRequired(), ])
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 256)])
    submit = SubmitField('Submit')

class AddForm(Form):
    category = SelectField('Category', coerce=int)
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 256)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in
                                 Category.query.order_by(Category.name).all()]
