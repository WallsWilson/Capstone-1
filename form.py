from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username')
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginFrom(FlaskForm):
    """Login form for login.html"""

    username = StringField('Username')
    password = PasswordField('Password', validators=[Length(min=6)])

class DrinkAddForm(FlaskForm):
    """Form to add a Drink and its recipe. This was not brough into the app yet."""

    drink_name = StringField('Drink Name')
    ingredients = StringField('Ingredients')
    instructions = StringField('Instructions')