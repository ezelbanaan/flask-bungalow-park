from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    week = SelectField('Desired week', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Book')

class UpdateBookingForm(FlaskForm):
    week = SelectField('Desired week', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Change')
