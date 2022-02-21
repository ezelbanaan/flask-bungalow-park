from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import DataRequired, ValidationError
from webapp.models import Bungalow

class AddBungalowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    bungalow_type = SelectField('Number of persons', choices=[('4', '4 People'), ('6', '6 People'), ('8', '8 People')], validators=[DataRequired()])
    weekprice = IntegerField('Weekly rate', widget=NumberInput(), validators=[DataRequired()])
    submit = SubmitField('Add bungalow')

    def validate_name(self, name):
        name = Bungalow.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('The chosen bungalow name already exists.')