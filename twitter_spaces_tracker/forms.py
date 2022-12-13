from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")


class AccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={'autofocus': True})
    token = PasswordField("Token", validators=[DataRequired()])
    submit = SubmitField("Track it!")

