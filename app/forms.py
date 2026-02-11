from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8)])

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Descripción', validators=[DataRequired(), Length(max=500)])