import os
import logging
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegisterForm, AlumnoForm, PreguntaForm, ExamenForm, BuscarAlumnoForm, BuscarGrupoForm
from config import DevelopmentConfig
from models import db, User, Alumno, Pregunta, Examen  
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuración de logging
LOG_FILENAME = os.path.join(LOG_DIR, "app.log")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILENAME)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# Configuración de logs mena
logging.info("Inicio de la aplicación")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Registro de inicio de la aplicación mena
app.logger.info("Inicio de la aplicación")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El usuario ya existe", "error")
            return redirect(url_for("register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        app.logger.info(f"Nuevo usuario registrado: {username}")

        flash("Usuario registrado correctamente.", "success")
        return redirect(url_for("register"))

    return render_template("register.html", form=form)

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()  

        if not user: 
            app.logger.warning(f"Intento de inicio de sesión con usuario inexistente: {username}")
            flash("El usuario no existe", "error")  # Mensaje de error
        elif not user.check_password(password):  
            app.logger.warning(f"Intento de inicio de sesión fallido para usuario: {username}")
            flash("Contraseña incorrecta", "error")  # Mensaje de error
        else:
            login_user(user)
            app.logger.info(f"Usuario {username} inició sesión")
            return redirect(url_for("layout"))  

    return render_template("login.html", form=form)

@app.route("/layout")
@login_required
def layout():
    return render_template("layout.html", user=current_user)  

@app.route("/logout")
@login_required
def logout():
    app.logger.info(f"Usuario {current_user.username} cerró sesión")
    logout_user()
    return redirect(url_for("login"))

@app.route("/registrar_alumno", methods=["GET", "POST"])
@login_required
def registrar_alumno():
    form = AlumnoForm()
    
    if form.validate_on_submit():
        nuevo_alumno = Alumno(
            nombre=form.nombre.data.strip(),
            apaterno=form.apaterno.data.strip(),
            amaterno=form.amaterno.data.strip() if form.amaterno.data else "",
            fecha_nacimiento=form.fecha_nacimiento.data,
            grupo=form.grupo.data
        )
        db.session.add(nuevo_alumno)
        db.session.commit()

        app.logger.info(f"Alumno registrado por {current_user.username}: {nuevo_alumno.nombre} {nuevo_alumno.apaterno}")

        flash("Alumno registrado con éxito", "success")
        return redirect(url_for('registrar_alumno'))
    
    return render_template('registrar_alumno.html', form=form)


@app.route("/agregar_pregunta", methods=["GET", "POST"])
@login_required
def agregar_pregunta():
    form = PreguntaForm()
    if form.validate_on_submit():
        nueva_pregunta = Pregunta(
            texto=form.texto.data,
            opcion_a=form.opcion_a.data,
            opcion_b=form.opcion_b.data,
            opcion_c=form.opcion_c.data,
            opcion_d=form.opcion_d.data,
            respuesta_correcta=form.respuesta_correcta.data
        )
        db.session.add(nueva_pregunta)
        db.session.commit()

        app.logger.info(f"Pregunta agregada por {current_user.username}: {nueva_pregunta.texto}")

        flash("Pregunta agregada con éxito", "success")
        return redirect(url_for('agregar_pregunta'))
    
    return render_template('agregar_pregunta.html', form=form)


@app.route("/realizar_examen", methods=["GET", "POST"])
@login_required
def realizar_examen():
    form = BuscarAlumnoForm()  
    alumno = None
    preguntas = []

    if form.validate_on_submit():
        alumno = Alumno.query.filter_by(nombre=form.nombre.data, apaterno=form.apaterno.data).first()
        if not alumno:
            flash('Alumno no encontrado', 'danger')
            return redirect(url_for('realizar_examen'))

        preguntas = Pregunta.query.all()
        return render_template('realizar_examen.html', form=form, alumno=alumno, preguntas=preguntas) 

    return render_template('buscar_alumno.html', form=form)  

@app.route("/guardar_examen", methods=["POST"])
@login_required
def guardar_examen():
    alumno_id = request.form.get('alumno_id')
    respuestas = []
    errores = []
    for pregunta in Pregunta.query.all():
        respuesta = request.form.get(f'respuesta_{pregunta.id}')
        if not respuesta:
            errores.append(pregunta.id) 
        respuestas.append(respuesta)

    if errores:
        alumno = Alumno.query.get(alumno_id)
        preguntas = Pregunta.query.all()
        form = BuscarAlumnoForm()
        return render_template('realizar_examen.html', alumno=alumno, preguntas=preguntas, errores=errores, form=form)

    preguntas = Pregunta.query.all()
    correctas = sum(1 for i, pregunta in enumerate(preguntas) if respuestas[i] == pregunta.respuesta_correcta)

    for i, pregunta in enumerate(preguntas):
        nueva_respuesta = Examen(alumno_id=alumno_id, pregunta_id=pregunta.id, respuesta=respuestas[i])
        db.session.add(nueva_respuesta)

    db.session.commit()

    app.logger.info(f"Examen guardado por {current_user.username} para alumno ID {alumno_id}")

    return render_template('espera_calificacion.html', alumno_id=alumno_id)

@app.route("/ver_calificaciones", methods=["GET", "POST"])
@login_required
def ver_calificaciones():
    form = BuscarGrupoForm()
    grupos_existentes = ['IDGS801', 'IDGS802', 'IDGS803', 'IDGS804', 'IDGS805']
    form.grupo.choices = [(grupo, grupo) for grupo in grupos_existentes]  

    grupo_seleccionado = None
    alumnos = []
    resultados = {}
    algun_examen_realizado = False 

    if request.method == 'POST':
        grupo_seleccionado = request.form.get('grupo')
        alumnos = Alumno.query.filter_by(grupo=grupo_seleccionado).all()
        if alumnos:
            for alumno in alumnos:
                respuestas = Examen.query.filter_by(alumno_id=alumno.id).all()
                total_preguntas = len(respuestas)
                correctas = sum(1 for respuesta in respuestas if Pregunta.query.get(respuesta.pregunta_id).respuesta_correcta == respuesta.respuesta)

                porcentaje = (correctas / total_preguntas) * 100 if total_preguntas > 0 else None
                resultados[alumno.id] = porcentaje
                if porcentaje is not None: 
                    algun_examen_realizado = True
        else:
            resultados = {}

    return render_template(
        'ver_calificaciones.html',
        form=form,
        grupos=grupos_existentes,
        alumnos=alumnos,
        grupo_seleccionado=grupo_seleccionado,
        resultados=resultados,
        algun_examen_realizado=algun_examen_realizado
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)