from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    amaterno = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date)
    grupo = db.Column(db.String(10))

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(255))
    opcion_a = db.Column(db.String(100))
    opcion_b = db.Column(db.String(100))
    opcion_c = db.Column(db.String(100))
    opcion_d = db.Column(db.String(100))
    respuesta_correcta = db.Column(db.String(1))

class Examen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))
    respuesta = db.Column(db.String(1))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_plain = db.Column(db.String(255), nullable=True)  
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_plain = password  
        self.password_hash = generate_password_hash(password)  

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
