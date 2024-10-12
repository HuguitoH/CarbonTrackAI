from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app import db, Mision  # Importar el modelo Mision y db

# Función para inicializar el scheduler
def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=crear_misiones_semanales, trigger="interval", weeks=1)  # Cada semana
    scheduler.add_job(func=crear_misiones_especiales, trigger="interval", days=2)  # Cada 48 horas
    scheduler.add_job(func=crear_misiones_tiempo_limitado, trigger="interval", days=1)  # Cada 24 horas
    scheduler.start()

# Funciones para crear misiones
def crear_misiones_semanales():
    nueva_mision1 = Mision(nombre="Apagar luces cuando no las uses", tipo="semanal", puntos=5, completada=False)
    nueva_mision2 = Mision(nombre="Usar bicicleta 3 veces a la semana", tipo="semanal", puntos=5, completada=False)
    db.session.add_all([nueva_mision1, nueva_mision2])
    db.session.commit()
    print("Misiones semanales creadas")

def crear_misiones_especiales():
    nueva_mision = Mision(nombre="Plantar 5 árboles en tu comunidad", tipo="especial", puntos=15, completada=False)
    db.session.add(nueva_mision)
    db.session.commit()
    print(f"Misión especial creada: {nueva_mision.nombre}")

def crear_misiones_tiempo_limitado():
    nueva_mision = Mision(nombre="Participar en la campaña 'Energía limpia'", tipo="tiempo_limitado", puntos=25, completada=False)
    db.session.add(nueva_mision)
    db.session.commit()
    print(f"Misión de tiempo limitado creada: {nueva_mision.nombre}")
