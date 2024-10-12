from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt
from datetime import timedelta
#from scheduler import iniciar_scheduler  # Importamos el scheduler
from datetime import datetime




app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbontrackai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Cambia esto por una clave secreta real
app.permanent_session_lifetime = timedelta(days=7)  # Tiempo de sesión de 7 días

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#iniciar_scheduler()


# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(50), nullable=False, default='default-avatar')
    password = db.Column(db.String(120), nullable=False)
    puntos = db.Column(db.Integer, default=0)
    nivel = db.Column(db.String(50), default='Beginner')
    tutorial_completado = db.Column(db.Boolean, default=False)
    
    # Nuevos campos para el progreso de las misiones
    progreso_semanales = db.Column(db.Integer, default=0)
    progreso_tiempo_limitado = db.Column(db.Integer, default=0)
    progreso_especiales = db.Column(db.Integer, default=0)

    
class CarbonFootprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    energy = db.Column(db.Float, default=0.0)
    food = db.Column(db.Float, default=0.0)
    walk = db.Column(db.Float, default=0.0)
    transport = db.Column(db.Float, default=0.0)

    usuario = db.relationship('Usuario', backref=db.backref('carbon_footprint', lazy=True))
    
# Tabla de misiones
class Mision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(50))  # 'semanal', 'especial', 'tiempo_limitado'
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    puntos = db.Column(db.Integer)
    completada = db.Column(db.Boolean, default=False)



# Ruta principal que renderiza el formulario de registro
@app.route('/')
def index():
    return render_template('index.html')

# Registro de usuario
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()  # Obtener los datos en formato JSON
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    # Validar que el email no exista ya en la base de datos
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({'error': 'El email ya está registrado.'}), 400

    # Validar que la contraseña no sea nula
    if not password:
        return jsonify({'error': 'La contraseña es requerida.'}), 400

    # Encriptar la contraseña antes de guardarla
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Crear un nuevo usuario
    nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password, avatar='default-avatar')
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Iniciar sesión automáticamente después del registro
    session['user_id'] = nuevo_usuario.id
    session['email'] = nuevo_usuario.email

    # Redirigir a la página de selección de avatar
    return jsonify({'message': 'Usuario registrado con éxito', 'redirect': url_for('seleccion_avatar')})


# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Recibimos los datos enviados desde el formulario de inicio de sesión
        email = data.get('email')
        password = data.get('password')

        # Buscar el usuario en la base de datos por su correo electrónico
        usuario = Usuario.query.filter_by(email=email).first()

        # Verificar que el usuario existe y que la contraseña es correcta
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.password):
            session['user_id'] = usuario.id  # Guardamos la información en la sesión
            session['email'] = usuario.email
            return jsonify({'message': 'Inicio de sesión exitoso', 'redirect': url_for('dashboard')})
        else:
            return jsonify({'error': 'Correo o contraseña incorrectos.'}), 401
    else:
        return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# Ruta para mostrar la página de selección de avatar
@app.route('/seleccion-avatar')
def seleccion_avatar():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template('seleccion-avatar.html')



@app.route('/guardar-avatar', methods=['POST'])
def guardar_avatar():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    data = request.get_json()
    avatar = data.get('avatar')
    avatar_color = data.get('color')  # Recibir el color
    avatar_image = data.get('image')  # Recibir la animación

    if not avatar:
        return jsonify({'error': 'No se ha enviado un avatar'}), 400

    # Actualizar el avatar y el color en la base de datos
    usuario = Usuario.query.get(session['user_id'])
    usuario.avatar = avatar
    usuario.avatar_color = avatar_color  # Guardar el color del avatar
    usuario.avatar_image = avatar_image  # Guardar la animación si es necesario

    db.session.commit()

    return jsonify({'success': True, 'message': 'Avatar, color y animación guardados correctamente'})

    # Redirigir a la encuesta después de guardar el avatar
    return jsonify({'success': True, 'redirect': url_for('encuesta')})


@app.route('/encuesta')
def encuesta():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Renderizar el template de la encuesta
    return render_template('encuesta.html')


@app.route('/crear-misiones-prueba')
def crear_misiones_prueba():
    misiones_prueba = [
        Mision(nombre="Prueba Semanal 1", tipo="semanal", puntos=5, completada=False),
        Mision(nombre="Prueba Tiempo Limitado 1", tipo="tiempo_limitado", puntos=25, completada=False),
        Mision(nombre="Prueba Especial 1", tipo="especial", puntos=15, completada=False)
    ]
    for mision in misiones_prueba:
        db.session.add(mision)
    db.session.commit()
    return "Misiones de prueba creadas con éxito"



@app.route('/guardar-huella', methods=['POST'])

def guardar_huella():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    usuario = Usuario.query.get(session['user_id'])

    # Recibir las respuestas del formulario
    energy_usage = int(request.form.get('energy_usage'))
    meat_consumption = int(request.form.get('meat_consumption'))
    walk_frequency = int(request.form.get('walk_frequency'))
    car_usage = int(request.form.get('car_usage'))

    # Asignar valores de huella basados en las respuestas
    huella = CarbonFootprint(
        user_id=usuario.id,
        energy=energy_usage * 10,  # Valor representativo
        food=meat_consumption * 15,
        walk=walk_frequency * 5,
        transport=car_usage * 20
    )

    # Guardar en la base de datos
    db.session.add(huella)
    db.session.commit()

    return redirect(url_for('dashboard'))  # Redirige al dashboard después de guardar


@app.route('/loader')
def loader():
    return render_template('loader.html')

@app.route('/misiones')
def misiones():
    # Obtener las misiones de la base de datos por tipo
    misiones_semanales = Mision.query.filter_by(tipo='semanal').all()
    misiones_especiales = Mision.query.filter_by(tipo='especial').all()
    misiones_tiempo_limitado = Mision.query.filter_by(tipo='tiempo_limitado').all()

    return render_template('misiones.html', 
                           misiones_semanales=misiones_semanales, 
                           misiones_especiales=misiones_especiales,
                           misiones_tiempo_limitado=misiones_tiempo_limitado)


@app.route('/update-mission', methods=['POST'])
def update_mission():
    data = request.get_json()
    print(data)  # Verifica qué datos están llegando

    mission_id = data.get('mission_id')
    completed = data.get('completed')
    
    print(f"Mission ID: {mission_id}, Completed: {completed}")  # Verifica si se está obteniendo correctamente

    # Buscar la misión en la base de datos usando el nuevo método Session.get()
    mision = db.session.get(Mision, mission_id)
    if not mision:
        print('Misión no encontrada')  # Log para verificar si está fallando aquí
        return jsonify({'success': False, 'message': 'Misión no encontrada'}), 404

    # Actualizar el estado de completada
    mision.completada = completed
    db.session.commit()

    print('Misión actualizada correctamente')  # Log de éxito

    return jsonify({'success': True, 'message': 'Misión actualizada correctamente'})




@app.route('/progreso-misiones', methods=['GET'])
def progreso_misiones():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    # Obtener las misiones completadas y el progreso para cada categoría
    misiones_semanales = Mision.query.filter_by(tipo='semanal').all()
    misiones_tiempo_limitado = Mision.query.filter_by(tipo='tiempo_limitado').all()
    misiones_especiales = Mision.query.filter_by(tipo='especial').all()

    # Calcular el progreso de cada categoría
    progreso_semanales = sum(mision.puntos for mision in misiones_semanales if mision.completada)
    progreso_tiempo_limitado = sum(mision.puntos for mision in misiones_tiempo_limitado if mision.completada)
    progreso_especiales = sum(mision.puntos for mision in misiones_especiales if mision.completada)

    # Definir los puntos máximos para cada tipo de misión
    max_puntos_semanales = sum(mision.puntos for mision in misiones_semanales)
    max_puntos_tiempo_limitado = sum(mision.puntos for mision in misiones_tiempo_limitado)
    max_puntos_especiales = sum(mision.puntos for mision in misiones_especiales)

    # Calcular el porcentaje de progreso
    porcentaje_semanales = (progreso_semanales / max_puntos_semanales) * 100 if max_puntos_semanales > 0 else 0
    porcentaje_tiempo_limitado = (progreso_tiempo_limitado / max_puntos_tiempo_limitado) * 100 if max_puntos_tiempo_limitado > 0 else 0
    porcentaje_especiales = (progreso_especiales / max_puntos_especiales) * 100 if max_puntos_especiales > 0 else 0

    return jsonify({
        'semanales': porcentaje_semanales,
        'tiempo_limitado': porcentaje_tiempo_limitado,
        'especiales': porcentaje_especiales
    })


# Ruta para mostrar el dashboard del usuario
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.get(session['user_id'])

    # Calcular los puntos de misiones completadas
    misiones_semanales = Mision.query.filter_by(tipo='semanal').all()
    misiones_tiempo_limitado = Mision.query.filter_by(tipo='tiempo_limitado').all()
    misiones_especiales = Mision.query.filter_by(tipo='especial').all()

    # Sumar los puntos de las misiones completadas
    puntos_semanales = sum(mision.puntos for mision in misiones_semanales if mision.completada)
    puntos_tiempo_limitado = sum(mision.puntos for mision in misiones_tiempo_limitado if mision.completada)
    puntos_especiales = sum(mision.puntos for mision in misiones_especiales if mision.completada)

    # Lógica para la huella de carbono (carbon footprint)
    huella = CarbonFootprint.query.filter_by(user_id=usuario.id).first()

    if huella:
        total = huella.energy + huella.food + huella.walk + huella.transport

        if total > 0:
            huella_datos = {
                'energy': (huella.energy / total) * 100,
                'food': (huella.food / total) * 100,
                'walk': (huella.walk / total) * 100,
                'transport': (huella.transport / total) * 100
            }
        else:
            huella_datos = {'energy': 0, 'food': 0, 'walk': 0, 'transport': 0}
    else:
        huella_datos = {'energy': 0, 'food': 0, 'walk': 0, 'transport': 0}

    # Pasamos los puntos al template del dashboard
    return render_template(
        'dashboard.html', 
        usuario=usuario, 
        huella_datos=huella_datos, 
        avatar=usuario.avatar, 
        puntos_semanales=puntos_semanales, 
        puntos_tiempo_limitado=puntos_tiempo_limitado, 
        puntos_especiales=puntos_especiales
    )





# Ruta para mostrar el tutorial
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Ruta para completar el tutorial
@app.route('/completar-tutorial', methods=['POST'])
def completar_tutorial():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    usuario = Usuario.query.get(session['user_id'])
    usuario.tutorial_completado = True
    db.session.commit()

    return jsonify({'success': True, 'message': 'Tutorial completado. Ahora puedes acceder al dashboard.'})

# Inicializar la base de datos
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas de la base de datos
    app.run(debug=True)