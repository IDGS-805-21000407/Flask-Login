from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3, max=15, message="Debe tener entre 3 y 15 caracteres")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="Este campo es obligatorio")
    ])
    submit = SubmitField("Iniciar Sesión")
