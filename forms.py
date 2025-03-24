from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3, max=15, message="Debe tener entre 3 y 15 caracteres")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="Este campo es obligatorio")
    ])
    submit = SubmitField("Iniciar Sesión")
    
    
class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(),
        Length(min=3, max=15)
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired()
    ])
    submit = SubmitField("Registrarse")


class AlumnoForm(FlaskForm):
    nombre = StringField('Nombre', [
        DataRequired(message='El campo es requerido'),
        Length(min=2, max=50, message='Longitud entre 2 y 50 caracteres')
    ])
    apaterno = StringField('Apellido Paterno', [DataRequired(message='El campo es requerido')])
    amaterno = StringField('Apellido Materno', [DataRequired(message='El campo es requerido')])  # 🔹 Agregado aquí
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[
        DataRequired(message='El campo es requerido')
    ])
    grupo = SelectField('Grupo', choices=[
        ('IDGS801', 'IDGS801'),
        ('IDGS802', 'IDGS802'),
        ('IDGS803', 'IDGS803'),
        ('IDGS804', 'IDGS804'),
        ('IDGS805', 'IDGS805')
    ], validators=[DataRequired(message='Seleccione un grupo')])
    
    submit = SubmitField('Guardar')
class PreguntaForm(FlaskForm):
    texto = StringField('Pregunta', [
        DataRequired(message='El campo es requerido'),
        Length(min=5, max=255, message='Longitud entre 5 y 255 caracteres')
    ])
    opcion_a = StringField('Opción A', [DataRequired(message='Requerido')])
    opcion_b = StringField('Opción B', [DataRequired(message='Requerido')])
    opcion_c = StringField('Opción C', [DataRequired(message='Requerido')])
    opcion_d = StringField('Opción D', [DataRequired(message='Requerido')])
    respuesta_correcta = SelectField('Respuesta Correcta', choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ], validators=[DataRequired(message='Selecciona una respuesta')])
    submit = SubmitField('Guardar')

class ExamenForm(FlaskForm):
    alumno_id = IntegerField('ID Alumno', validators=[
        DataRequired(message='El ID del alumno es obligatorio'),
        NumberRange(min=1, message='ID inválido')
    ])
    pregunta_id = IntegerField('ID Pregunta', validators=[
        DataRequired(message='El ID de la pregunta es obligatorio'),
        NumberRange(min=1, message='ID inválido')
    ])
    respuesta = SelectField('Respuesta', choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ], validators=[DataRequired(message='Selecciona una respuesta')])
    submit = SubmitField('Enviar')

class BuscarAlumnoForm(FlaskForm):
    nombre = StringField('Nombre', [DataRequired(message='Ingresa el nombre')])
    apaterno = StringField('Apellido Paterno', [DataRequired(message='Ingresa el apellido paterno')])
    submit = SubmitField('Buscar')
    
class BuscarGrupoForm(FlaskForm):
    grupo = SelectField('Grupo', choices=[], validators=[DataRequired()])
