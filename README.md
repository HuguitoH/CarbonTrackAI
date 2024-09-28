# CarbonTrackAI

**CarbonTrackAI** es una aplicación móvil multiplataforma que permite a los usuarios rastrear su huella de carbono diaria mediante la introducción de sus actividades cotidianas como el transporte, la alimentación, y el consumo energético. Utilizando inteligencia artificial (IA), ofrece recomendaciones personalizadas para reducir el impacto ambiental. Además, fomenta la gamificación con logros, retos y tablas de clasificación, creando una comunidad que se compromete a combatir el cambio climático de forma divertida.

## 🚀 Funcionalidades Principales

- **Rastreo de Actividades Diarias**: Transporte, alimentación, consumo energético, y compras.
- **Cálculo de Huella de Carbono**: Basado en los datos ingresados por el usuario.
- **Recomendaciones Personalizadas con IA**: La IA ofrece sugerencias sobre cómo reducir la huella de carbono.
- **Gamificación**: Logros, retos, puntos y tablas de clasificación que motivan a reducir el impacto ambiental.
- **Visualización de Progreso**: Gráficas detalladas que muestran el progreso diario, semanal y mensual.

## 🛠️ Tecnologías Utilizadas

### Frontend
- **React Native**: Para el desarrollo de la aplicación móvil multiplataforma (iOS y Android).

### Backend
- **Python** con **Flask**: Para la lógica del servidor y el manejo de la API.
  
### Inteligencia Artificial
- **TensorFlow**: Para el desarrollo de los modelos de IA que generan recomendaciones personalizadas.

### Base de Datos
- **PostgreSQL**: Base de datos relacional para almacenar los datos de los usuarios y sus actividades.

### Otros
- **Firebase**: Para la autenticación de usuarios y almacenamiento en tiempo real (opcional).
- **Heroku/AWS**: Despliegue del backend.

## 📦 Instalación y Configuración

### Requisitos

- **Node.js** (v14 o superior)
- **Python 3.x**
- **PostgreSQL** (v13 o superior)
- **Git**

### Instalación del Frontend (React Native)

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/CarbonTrackAI.git
    cd CarbonTrackAI/mobile
    ```

2. Instala las dependencias:
    ```bash
    npm install
    ```

3. Ejecuta la aplicación en un emulador o dispositivo:
    ```bash
    npx react-native run-android  # Para Android
    npx react-native run-ios  # Para iOS (en Mac)
    ```

### Instalación del Backend (Flask)

1. Clona el repositorio si no lo has hecho ya:
    ```bash
    git clone https://github.com/tu-usuario/CarbonTrackAI.git
    cd CarbonTrackAI/app
    ```

2. Crea un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura PostgreSQL:
    - Crea la base de datos:
      ```bash
      createdb huella_carbono_db
      ```

    - Actualiza la cadena de conexión en `app.py`:
      ```python
      app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tu_usuario:tu_password@localhost/huella_carbono_db'
      ```

5. Inicia el servidor Flask:
    ```bash
    python app.py
    ```

El backend debería estar disponible en `http://127.0.0.1:5000`.

## 🚀 Despliegue

### Despliegue en Heroku

1. Inicia sesión en Heroku:
    ```bash
    heroku login
    ```

2. Crea una nueva aplicación en Heroku:
    ```bash
    heroku create
    ```

3. Despliega el proyecto en Heroku:
    ```bash
    git push heroku master
    ```

4. Abre la aplicación en el navegador:
    ```bash
    heroku open
    ```

### Despliegue en AWS (Opcional)
Para desplegar en AWS, sigue la [documentación oficial de AWS](https://aws.amazon.com/getting-started/).

## 📚 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas o encuentras problemas, por favor, abre un **issue** o envía un **pull request**.

1. Haz un **fork** del proyecto.
2. Crea una nueva rama para tus cambios:
    ```bash
    git checkout -b mi-nueva-funcionalidad
    ```
3. Realiza los cambios y añade los **commits**:
    ```bash
    git commit -m "Añadí una nueva funcionalidad"
    ```
4. Sube los cambios a tu repositorio:
    ```bash
    git push origin mi-nueva-funcionalidad
    ```
5. Abre un **pull request** en GitHub.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Revisa el archivo [LICENSE](LICENSE) para más información.

## 💡 Contacto

Si tienes preguntas o sugerencias, no dudes en contactar conmigo a través de [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com) o abrir un **issue** en el repositorio.

---

## 🌍 ¡Únete al Cambio!

Con **CarbonTrackAI**, estamos trabajando para construir un futuro más sostenible. Tu contribución a reducir la huella de carbono no solo tiene un impacto positivo en el medio ambiente, sino que también te conecta con una comunidad global comprometida con el cambio. ¡Gracias por unirte a esta misión!

