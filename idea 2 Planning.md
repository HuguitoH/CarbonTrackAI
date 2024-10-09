Plan para comenzar:
Configurar el Backend (Flask + PostgreSQL)
Crear la API para gestionar la huella de carbono, usuarios, misiones diarias y la evolución del avatar.
Configurar el Frontend (React Native)
Desarrollar las pantallas principales: selección del avatar, huella de carbono, progreso y misiones.
Animación del Avatar (usando Lottie o animaciones SVG)
Integrar los avatares de Oso Polar, Águila, y Ballena y sus respectivas animaciones.


**Backend (Flask + PostgreSQL)**

- Estructura: 

CarbonTrackAI-backend/
├── app.py                   # Lógica principal del servidor
├── models.py                # Modelos de base de datos (Usuario, Misiones, Avatar)
├── requirements.txt         # Dependencias
└── venv/                    # Entorno virtual de Python


-Dependecias: 

python -m venv venv
source venv/bin/activate  # O venv\Scripts\activate en Windows
pip install Flask SQLAlchemy psycopg2


-App.py: 

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Mision, Avatar

app = Flask(__name__)

# Configuración de la base de datos (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tu_usuario:tu_password@localhost/carbontrackai_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Ruta principal
@app.route('/')
def home():
    return "¡Bienvenido a CarbonTrackAI!"

# Ruta para registrar un usuario y seleccionar su avatar
@app.route('/registro', methods=['POST'])
def registro():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    avatar_seleccionado = data.get('avatar')

    nuevo_usuario = Usuario(nombre=nombre, email=email, puntos=0, avatar=avatar_seleccionado, nivel='Novato')
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'message': f'Usuario {nombre} registrado exitosamente.'})

# Ruta para calcular huella de carbono
@app.route('/calcular_huella', methods=['POST'])
def calcular_huella():
    data = request.json
    energia = data.get('energia', 0)
    km_transporte = data.get('km_transporte', 0)
    dieta = data.get('dieta', 'normal')

    huella = energia * 0.5 + km_transporte * 0.21 + (2 if dieta == 'vegetariana' else 5)
    return jsonify({'huella': huella})

# Ruta para ver las misiones diarias
@app.route('/retos_diarios', methods=['GET'])
def retos_diarios():
    retos = Mision.query.all()
    lista_retos = [{'descripcion': reto.descripcion, 'puntos': reto.puntos} for reto in retos]
    return jsonify(lista_retos)

# Ruta para completar una misión
@app.route('/completar_reto', methods=['POST'])
def completar_reto():
    data = request.json
    reto_id = data.get('reto_id')
    usuario_id = data.get('usuario_id')

    usuario = Usuario.query.get(usuario_id)
    reto = Mision.query.get(reto_id)

    if reto:
        usuario.puntos += reto.puntos
        db.session.commit()

    return jsonify({'puntos_totales': usuario.puntos})

if __name__ == '__main__':
    app.run(debug=True)


. models.py:

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    puntos = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String(50), nullable=False)  # Avatar seleccionado (Oso Polar, Águila, Ballena)
    nivel = db.Column(db.String(50), default='Novato')

# Modelo de Mision
class Mision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    puntos = db.Column(db.Integer, nullable=False)

# Modelo de Avatar (puede usarse para guardar el estado de evolución del avatar)
class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # Ejemplo: Oso Polar, Águila, Ballena
    estado = db.Column(db.String(50), nullable=False, default="Inicial")  # Estado del avatar (Inicial, Evolución 1, 2)


- Base (PostgreSQL)

createdb carbontrackai_db

-Migraciones: 
flask db init
flask db migrate
flask db upgrade


**Frontend**

- React Native: 
npx react-native init CarbonTrackAI-mobile
cd CarbonTrackAI-mobile


- Dependecias: 

npm install axios react-navigation react-native-chart-kit react-native-svg lottie-react-native

-Selección de Avatar (SeleccionAvatar.js): 

import React, { useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function SeleccionAvatar({ navigation }) {
  const [avatarSeleccionado, setAvatarSeleccionado] = useState('');

  const seleccionarAvatar = (avatar) => {
    setAvatarSeleccionado(avatar);
    // Navegar a la pantalla principal de la app
    navigation.navigate('HuellaCarbono', { avatar: avatar });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Selecciona tu Avatar</Text>
      <Button title="Oso Polar" onPress={() => seleccionarAvatar('Oso Polar')} />
      <Button title="Águila" onPress={() => seleccionarAvatar('Águila')} />
      <Button title="Ballena" onPress={() => seleccionarAvatar('Ballena')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
});


-Home (HuellaCarbono.js):

import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

export default function HuellaCarbono({ route, navigation }) {
  const { avatar } = route.params;  // Avatar seleccionado
  const [huella, setHuella] = useState(0);
  const [data, setData] = useState([0, 0, 0, 0, 0, 0, 0]);

  useEffect(() => {
    // Aquí llamaremos a la API para obtener la huella de carbono y actualizar los datos del gráfico
    // Simulación de datos
    setData([20, 30, 25, 40, 50, 45, 60]);
    setHuella(45); // Simulación de huella
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tu Avatar: {avatar}</Text>

      <Text style={styles.subTitle}>Huella de Carbono Actual: {huella} kg CO₂</Text>

      <LineChart
        data={{
          labels: ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
          datasets: [{ data }]
        }}
        width={Dimensions.get("window").width - 20}
        height={220}
        chartConfig={{
          backgroundColor: "#e26a00",
          backgroundGradientFrom: "#fb8c00",
          backgroundGradientTo: "#ffa726",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
        style={{ marginVertical: 8, borderRadius: 16 }}
      />

      <View style={styles.categories}>
        <Text style={styles.categoryTitle}>Categorías Clave:</Text>
        <Text style={styles.category}>Transporte: 12 kg CO₂</Text>
        <Text style={styles.category}>Alimentación: 25 kg CO₂</Text>
        <Text style={styles.category}>Energía: 8 kg CO₂</Text>
      </View>

      <Button title="Ver Misiones" onPress={() => navigation.navigate('Misiones')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  subTitle: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  categories: {
    marginTop: 20,
  },
  categoryTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  category: {
    fontSize: 16,
    marginVertical: 5,
  },
});


-Misssions (Misiones.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import axios from 'axios';

export default function Misiones({ navigation }) {
  const [misiones, setMisiones] = useState([]);
  const [puntos, setPuntos] = useState(0);

  useEffect(() => {
    // Aquí llamaremos a la API para obtener las misiones diarias
    const obtenerMisiones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_diarios');
        setMisiones(response.data);
      } catch (error) {
        console.error('Error al obtener las misiones', error);
      }
    };
    obtenerMisiones();
  }, []);

  const completarMision = async (id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/completar_reto', { reto_id: id });
      setPuntos(response.data.puntos_totales);
    } catch (error) {
      console.error('Error al completar la misión', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Misiones Diarias</Text>

      {misiones.map((mision, index) => (
        <View key={index} style={styles.mision}>
          <Text>{mision.descripcion}</Text>
          <Button title="Completar" onPress={() => completarMision(index)} />
        </View>
      ))}

      <Text style={styles.puntos}>Puntos Totales: {puntos}</Text>
      <Button title="Regresar a la Huella de Carbono" onPress={() => navigation.goBack()} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  mision: {
    marginBottom: 15,
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  puntos: {
    marginTop: 20,
    fontSize: 18,
    textAlign: 'center',
  },
});


-Progreso (Progreso.js):

import React from 'react';
import { View, Text, Dimensions } from 'react-native';
import { BarChart } from 'react-native-chart-kit';

export default function Progreso() {
  const data = {
    labels: ["Transporte", "Alimentación", "Energía"],
    datasets: [
      {
        data: [50, 100, 40]  // Simulación de datos de huella
      }
    ]
  };

  return (
    <View>
      <Text style={{ fontSize: 24, textAlign: 'center', margin: 20 }}>Tu Progreso</Text>
      <BarChart
        data={data}
        width={Dimensions.get("window").width - 20}
        height={220}
        chartConfig={{
          backgroundColor: "#e26a00",
          backgroundGradientFrom: "#fb8c00",
          backgroundGradientTo: "#ffa726",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
        style={{ marginVertical: 8, borderRadius: 16 }}
      />
    </View>
  );
}

- Animar el avatar animal (Oso Polar, Águila, Ballena):

npm install lottie-react-native


-Animacion avatar pantalla principal: 

import React from 'react';
import { View, Text } from 'react-native';
import LottieView from 'lottie-react-native';

export default function AvatarAnimado({ avatar }) {
  return (
    <View style={{ alignItems: 'center' }}>
      <Text>Tu Avatar: {avatar}</Text>
      <LottieView
        source={require('../assets/animations/' + avatar + '.json')}  // Ruta de la animación
        autoPlay
        loop
        style={{ width: 150, height: 150 }}
      />
    </View>
  );
}


- Navigation (MainNavigator.js): 

import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';

import SeleccionAvatar from '../screens/SeleccionAvatar';
import HuellaCarbono from '../screens/HuellaCarbono';
import Misiones from '../screens/Misiones';
import Progreso from '../screens/Progreso';

const Stack = createStackNavigator();

export default function MainNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SeleccionAvatar">
        <Stack.Screen name="SeleccionAvatar" component={SeleccionAvatar} options={{ title: 'Selecciona tu Avatar' }} />
        <Stack.Screen name="HuellaCarbono" component={HuellaCarbono} options={{ title: 'Huella de Carbono' }} />
        <Stack.Screen name="Misiones" component={Misiones} options={{ title: 'Misiones Diarias' }} />
        <Stack.Screen name="Progreso" component={Progreso} options={{ title: 'Progreso' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


- App.js: (conectar navigation --> app.js) 

import React from 'react';
import MainNavigator from './src/navigation/MainNavigator';

export default function App() {
  return <MainNavigator />;
}


- Conectar API con misiones: 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import axios from 'axios';

export default function Misiones({ navigation }) {
  const [misiones, setMisiones] = useState([]);
  const [puntos, setPuntos] = useState(0);

  useEffect(() => {
    // Llamada a la API para obtener las misiones diarias
    const obtenerMisiones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_diarios');
        setMisiones(response.data);
      } catch (error) {
        console.error('Error al obtener las misiones', error);
      }
    };
    obtenerMisiones();
  }, []);

  const completarMision = async (id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/completar_reto', { reto_id: id });
      setPuntos(response.data.puntos_totales);
    } catch (error) {
      console.error('Error al completar la misión', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Misiones Diarias</Text>

      {misiones.map((mision, index) => (
        <View key={index} style={styles.mision}>
          <Text>{mision.descripcion}</Text>
          <Button title="Completar" onPress={() => completarMision(index)} />
        </View>
      ))}

      <Text style={styles.puntos}>Puntos Totales: {puntos}</Text>
      <Button title="Regresar a la Huella de Carbono" onPress={() => navigation.goBack()} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  mision: {
    marginBottom: 15,
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  puntos: {
    marginTop: 20,
    fontSize: 18,
    textAlign: 'center',
  },
});


- Actualizar Huella de CArbono:  (HuellaCarbono.js)

import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import axios from 'axios';

export default function HuellaCarbono({ route, navigation }) {
  const { avatar } = route.params;  // Avatar seleccionado
  const [huella, setHuella] = useState(0);
  const [data, setData] = useState([0, 0, 0, 0, 0, 0, 0]);
  const [categorias, setCategorias] = useState({
    transporte: 0,
    alimentacion: 0,
    energia: 0,
  });

  useEffect(() => {
    // Llamada a la API para obtener los datos de huella de carbono
    const obtenerHuella = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/calcular_huella', {
          energia: 100, // Simulación
          km_transporte: 50,  // Simulación
          dieta: 'normal'  // Simulación
        });
        setHuella(response.data.huella);

        // Simulación de los datos de las categorías
        setCategorias({
          transporte: 50,
          alimentacion: 30,
          energia: 20
        });

        // Simulación de los datos del gráfico
        setData([20, 30, 25, 40, 50, 45, 60]);
      } catch (error) {
        console.error('Error al obtener los datos de huella', error);
      }
    };

    obtenerHuella();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tu Avatar: {avatar}</Text>

      <Text style={styles.subTitle}>Huella de Carbono Actual: {huella} kg CO₂</Text>

      <LineChart
        data={{
          labels: ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
          datasets: [{ data }]
        }}
        width={Dimensions.get("window").width - 20}
        height={220}
        chartConfig={{
          backgroundColor: "#e26a00",
          backgroundGradientFrom: "#fb8c00",
          backgroundGradientTo: "#ffa726",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
        style={{ marginVertical: 8, borderRadius: 16 }}
      />

      <View style={styles.categories}>
        <Text style={styles.categoryTitle}>Categorías Clave:</Text>
        <Text style={styles.category}>Transporte: {categorias.transporte} kg CO₂</Text>
        <Text style={styles.category}>Alimentación: {categorias.alimentacion} kg CO₂</Text>
        <Text style={styles.category}>Energía: {categorias.energia} kg CO₂</Text>
      </View>

      <Button title="Ver Misiones" onPress={() => navigation.navigate('Misiones')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  subTitle: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  categories: {
    marginTop: 20,
  },
  categoryTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  category: {
    fontSize: 16,
    marginVertical: 5,
  },
});

- Animación Lottie: (AvatarAnimado.js)

import React from 'react';
import { View, Text } from 'react-native';
import LottieView from 'lottie-react-native';

export default function AvatarAnimado({ avatar }) {
  return (
    <View style={{ alignItems: 'center' }}>
      <Text>Tu Avatar: {avatar}</Text>
      <LottieView
        source={require('../assets/animations/' + avatar + '.json')}  // Ruta de la animación
        autoPlay
        loop
        style={{ width: 150, height: 150 }}
      />
    </View>
  );
}


- Mostrar avatar en huella Carbono (HuellaCarbono.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import axios from 'axios';
import AvatarAnimado from '../components/AvatarAnimado';  // Importamos el componente de animación

export default function HuellaCarbono({ route, navigation }) {
  const { avatar } = route.params;  // Avatar seleccionado
  const [huella, setHuella] = useState(0);
  const [data, setData] = useState([0, 0, 0, 0, 0, 0, 0]);
  const [categorias, setCategorias] = useState({
    transporte: 0,
    alimentacion: 0,
    energia: 0,
  });

  useEffect(() => {
    const obtenerHuella = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/calcular_huella', {
          energia: 100, 
          km_transporte: 50,  
          dieta: 'normal'
        });
        setHuella(response.data.huella);

        setCategorias({
          transporte: 50,
          alimentacion: 30,
          energia: 20
        });

        setData([20, 30, 25, 40, 50, 45, 60]);
      } catch (error) {
        console.error('Error al obtener los datos de huella', error);
      }
    };

    obtenerHuella();
  }, []);

  return (
    <View style={styles.container}>
      <AvatarAnimado avatar={avatar} />  {/* Mostramos la animación del avatar */}

      <Text style={styles.subTitle}>Huella de Carbono Actual: {huella} kg CO₂</Text>

      <LineChart
        data={{
          labels: ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
          datasets: [{ data }]
        }}
        width={Dimensions.get("window").width - 20}
        height={220}
        chartConfig={{
          backgroundColor: "#e26a00",
          backgroundGradientFrom: "#fb8c00",
          backgroundGradientTo: "#ffa726",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
        style={{ marginVertical: 8, borderRadius: 16 }}
      />

      <View style={styles.categories}>
        <Text style={styles.categoryTitle}>Categorías Clave:</Text>
        <Text style={styles.category}>Transporte: {categorias.transporte} kg CO₂</Text>
        <Text style={styles.category}>Alimentación: {categorias.alimentacion} kg CO₂</Text>
        <Text style={styles.category}>Energía: {categorias.energia} kg CO₂</Text>
      </View>

      <Button title="Ver Misiones" onPress={() => navigation.navigate('Misiones')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  subTitle: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  categories: {
    marginTop: 20,
  },
  categoryTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  category: {
    fontSize: 16,
    marginVertical: 5,
  },
});


- Recompensas y logros: (models.py)

# Modelo de Logro
class Logro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    puntos_necesarios = db.Column(db.Integer, nullable=False)
    recompensa = db.Column(db.String(255), nullable=False)  # Podría ser una medalla o evolución de avatar

- Ruta Backend logros: (app.py)

@app.route('/logros', methods=['GET'])
def obtener_logros():
    logros = Logro.query.all()
    lista_logros = [{'descripcion': logro.descripcion, 'puntos_necesarios': logro.puntos_necesarios, 'recompensa': logro.recompensa} for logro in logros]
    return jsonify(lista_logros)


- Ruta backend logros dar: (app.py)

@app.route('/otorgar_logro', methods=['POST'])
def otorgar_logro():
    data = request.json
    usuario_id = data.get('usuario_id')
    logro_id = data.get('logro_id')

    usuario = Usuario.query.get(usuario_id)
    logro = Logro.query.get(logro_id)

    if usuario.puntos >= logro.puntos_necesarios:
        # Aquí podrías guardar el logro en el historial del usuario
        return jsonify({'message': f'¡Logro alcanzado: {logro.descripcion}!', 'recompensa': logro.recompensa})
    else:
        return jsonify({'message': 'Aún no has alcanzado este logro.'})

- Frotend Logros (Logros.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import axios from 'axios';

export default function Logros() {
  const [logros, setLogros] = useState([]);

  useEffect(() => {
    const obtenerLogros = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/logros');
        setLogros(response.data);
      } catch (error) {
        console.error('Error al obtener los logros', error);
      }
    };
    obtenerLogros();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Logros Disponibles</Text>
      <FlatList
        data={logros}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.logro}>
            <Text style={styles.descripcion}>{item.descripcion}</Text>
            <Text style={styles.puntos}>Puntos necesarios: {item.puntos_necesarios}</Text>
            <Text style={styles.recompensa}>Recompensa: {item.recompensa}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  logro: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  descripcion: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  puntos: {
    fontSize: 16,
    marginVertical: 5,
  },
  recompensa: {
    fontSize: 16,
    color: '#2e7d32',
  },
});


- Implemnetación Logro (MainNavigator.js): 

import Logros from '../screens/Logros';  // Importamos la pantalla de logros

export default function MainNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SeleccionAvatar">
        <Stack.Screen name="SeleccionAvatar" component={SeleccionAvatar} options={{ title: 'Selecciona tu Avatar' }} />
        <Stack.Screen name="HuellaCarbono" component={HuellaCarbono} options={{ title: 'Huella de Carbono' }} />
        <Stack.Screen name="Misiones" component={Misiones} options={{ title: 'Misiones Diarias' }} />
        <Stack.Screen name="Progreso" component={Progreso} options={{ title: 'Progreso' }} />
        <Stack.Screen name="Logros" component={Logros} options={{ title: 'Logros Disponibles' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

-Boton logros en Heulla de carbono (HuellaCarbono.js): 

<Button title="Ver Logros" onPress={() => navigation.navigate('Logros')} />


- Evolución del Avatar según el Progreso  (models.py): 

class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # Ejemplo: Oso Polar, Águila, Ballena
    estado = db.Column(db.String(50), nullable=False, default="Inicial")  # Estado del avatar (Inicial, Evolución 1, 2)
    puntos_necesarios_para_evolucion = db.Column(db.Integer, default=100)  # Puntos necesarios para la evolución


- Evolución de avatar backend (app.py):

@app.route('/evolucion_avatar', methods=['POST'])
def evolucionar_avatar():
    data = request.json
    usuario_id = data.get('usuario_id')

    usuario = Usuario.query.get(usuario_id)
    avatar = Avatar.query.filter_by(tipo=usuario.avatar).first()

    if usuario.puntos >= avatar.puntos_necesarios_para_evolucion:
        avatar.estado = "Evolución 1"  # Se podría manejar más estados
        db.session.commit()
        return jsonify({'message': f'¡Tu {avatar.tipo} ha evolucionado a {avatar.estado}!', 'estado': avatar.estado})
    else:
        return jsonify({'message': 'Aún no tienes suficientes puntos para evolucionar.'})


-Actualizar evolución (AvatarAnimado.js): 

import React, { useState, useEffect } from 'react';
import { View, Text } from 'react-native';
import LottieView from 'lottie-react-native';
import axios from 'axios';

export default function AvatarAnimado({ avatar }) {
  const [estado, setEstado] = useState('Inicial');

  useEffect(() => {
    const obtenerEstadoAvatar = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/evolucion_avatar', { usuario_id: 1 });  // Simulación de usuario
        setEstado(response.data.estado);
      } catch (error) {
        console.error('Error al obtener el estado del avatar', error);
      }
    };
    obtenerEstadoAvatar();
  }, []);

  return (
    <View style={{ alignItems: 'center' }}>
      <Text>Tu Avatar: {avatar} - Estado: {estado}</Text>
      <LottieView
        source={require('../assets/animations/' + avatar + '-' + estado + '.json')}  // Ruta de la animación según estado
        autoPlay
        loop
        style={{ width: 150, height: 150 }}
      />
    </View>
  );
}


- Notificaciones (Misiones.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';
import axios from 'axios';

export default function Misiones({ navigation }) {
  const [misiones, setMisiones] = useState([]);
  const [puntos, setPuntos] = useState(0);

  useEffect(() => {
    const obtenerMisiones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_diarios');
        setMisiones(response.data);
      } catch (error) {
        console.error('Error al obtener las misiones', error);
      }
    };
    obtenerMisiones();
  }, []);

  const completarMision = async (id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/completar_reto', { reto_id: id });
      setPuntos(response.data.puntos_totales);

      // Mostrar una alerta cuando el usuario completa una misión
      Alert.alert(
        "¡Misión completada!",
        `Has completado una misión y has ganado ${response.data.puntos_totales} puntos.`,
        [{ text: "OK", onPress: () => console.log("OK Pressed") }]
      );
    } catch (error) {
      console.error('Error al completar la misión', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Misiones Diarias</Text>

      {misiones.map((mision, index) => (
        <View key={index} style={styles.mision}>
          <Text>{mision.descripcion}</Text>
          <Button title="Completar" onPress={() => completarMision(index)} />
        </View>
      ))}

      <Text style={styles.puntos}>Puntos Totales: {puntos}</Text>
      <Button title="Regresar a la Huella de Carbono" onPress={() => navigation.goBack()} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign


- Notificación evoucion avatar (HuellaCarbono.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import axios from 'axios';
import AvatarAnimado from '../components/AvatarAnimado';

export default function HuellaCarbono({ route, navigation }) {
  const { avatar } = route.params;
  const [huella, setHuella] = useState(0);
  const [data, setData] = useState([0, 0, 0, 0, 0, 0, 0]);
  const [estadoAvatar, setEstadoAvatar] = useState('Inicial');
  const [categorias, setCategorias] = useState({
    transporte: 0,
    alimentacion: 0,
    energia: 0,
  });

  useEffect(() => {
    const obtenerHuella = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/calcular_huella', {
          energia: 100,
          km_transporte: 50,
          dieta: 'normal'
        });
        setHuella(response.data.huella);

        setCategorias({
          transporte: 50,
          alimentacion: 30,
          energia: 20
        });

        setData([20, 30, 25, 40, 50, 45, 60]);
      } catch (error) {
        console.error('Error al obtener los datos de huella', error);
      }
    };

    obtenerHuella();

    // Verificar si el avatar ha evolucionado
    const verificarEvolucionAvatar = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/evolucion_avatar', { usuario_id: 1 });
        if (response.data.estado !== estadoAvatar) {
          setEstadoAvatar(response.data.estado);

          // Mostrar alerta de evolución del avatar
          Alert.alert(
            "¡Tu avatar ha evolucionado!",
            `¡Tu ${avatar} ha alcanzado el estado: ${response.data.estado}!`,
            [{ text: "OK", onPress: () => console.log("OK Pressed") }]
          );
        }
      } catch (error) {
        console.error('Error al verificar la evolución del avatar', error);
      }
    };

    verificarEvolucionAvatar();
  }, [estadoAvatar]);

  return (
    <View style={styles.container}>
      <AvatarAnimado avatar={avatar} estado={estadoAvatar} />

      <Text style={styles.subTitle}>Huella de Carbono Actual: {huella} kg CO₂</Text>

      <LineChart
        data={{
          labels: ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
          datasets: [{ data }]
        }}
        width={Dimensions.get("window").width - 20}
        height={220}
        chartConfig={{
          backgroundColor: "#e26a00",
          backgroundGradientFrom: "#fb8c00",
          backgroundGradientTo: "#ffa726",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
        style={{ marginVertical: 8, borderRadius: 16 }}
      />

      <View style={styles.categories}>
        <Text style={styles.categoryTitle}>Categorías Clave:</Text>
        <Text style={styles.category}>Transporte: {categorias.transporte} kg CO₂</Text>
        <Text style={styles.category}>Alimentación: {categorias.alimentacion} kg CO₂</Text>
        <Text style={styles.category}>Energía: {categorias.energia} kg CO₂</Text>
      </View>

      <Button title="Ver Misiones" onPress={() => navigation.navigate('Misiones')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  subTitle: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  categories: {
    marginTop: 20,
  },
  categoryTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  category: {
    fontSize: 16,
    marginVertical: 5,
  },
});


- Mejora en transiciones: (MainNavigator.js)

const Stack = createStackNavigator();

export default function MainNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="SeleccionAvatar"
        screenOptions={{
          headerShown: false,
          transitionSpec: {
            open: { animation: 'timing', config: { duration: 500 } },
            close: { animation: 'timing', config: { duration: 500 } },
          },
        }}>
        <Stack.Screen name="SeleccionAvatar" component={SeleccionAvatar} />
        <Stack.Screen name="HuellaCarbono" component={HuellaCarbono} />
        <Stack.Screen name="Misiones" component={Misiones} />
        <Stack.Screen name="Progreso" component={Progreso} />
        <Stack.Screen name="Logros" component={Logros} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


- Animaciones en las misiones completadas (Misiones.js): 

import LottieView from 'lottie-react-native';

const completarMision = async (id) => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/completar_reto', { reto_id: id });
    setPuntos(response.data.puntos_totales);

    // Mostrar una animación al completar una misión
    Alert.alert(
      "¡Misión completada!",
      `Has completado una misión y has ganado ${response.data.puntos_totales} puntos.`,
      [{ text: "OK", onPress: () => console.log("OK Pressed") }]
    );

    // Iniciar la animación de éxito
    this.animation.play();
  } catch (error) {
    console.error('Error al completar la misión', error);
  }
};

return (
  <View style={styles.container}>
    <LottieView
      ref={animation => { this.animation = animation; }}
      source={require('../assets/animations/success.json')}
      loop={false}
      style={{ width: 100, height: 100, alignSelf: 'center' }}
    />
    {/* Resto de la pantalla de misiones */}
  </View>
);


- Medallas Misiones (Misiones.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';
import LottieView from 'lottie-react-native';
import axios from 'axios';

export default function Misiones({ navigation }) {
  const [misiones, setMisiones] = useState([]);
  const [puntos, setPuntos] = useState(0);

  useEffect(() => {
    const obtenerMisiones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_diarios');
        setMisiones(response.data);
      } catch (error) {
        console.error('Error al obtener las misiones', error);
      }
    };
    obtenerMisiones();
  }, []);

  const completarMision = async (id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/completar_reto', { reto_id: id });
      setPuntos(response.data.puntos_totales);

      // Mostrar notificación visual
      Alert.alert(
        "¡Misión completada!",
        `Has completado una misión y has ganado ${response.data.puntos_totales} puntos.`,
        [{ text: "OK", onPress: () => console.log("OK Pressed") }]
      );

      // Iniciar la animación de medalla
      this.animation.play();
    } catch (error) {
      console.error('Error al completar la misión', error);
    }
  };

  return (
    <View style={styles.container}>
      <LottieView
        ref={animation => { this.animation = animation; }}
        source={require('../assets/animations/medal.json')}
        loop={false}
        style={{ width: 150, height: 150, alignSelf: 'center', marginBottom: 20 }}
      />

      {misiones.map((mision, index) => (
        <View key={index} style={styles.mision}>
          <Text>{mision.descripcion}</Text>
          <Button title="Completar" onPress={() => completarMision(index)} />
        </View>
      ))}

      <Text style={styles.puntos}>Puntos Totales: {puntos}</Text>
      <Button title="Regresar a la Huella de Carbono" onPress={() => navigation.goBack()} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  mision: {
    marginBottom: 15,
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  puntos: {
    marginTop: 20,
    fontSize: 18,
    textAlign: 'center',
  },
});


- Gráficos más detallados en la pantalla de progreso (Progreso.js): 

import React from 'react';
import { View, Text, Dimensions } from 'react-native';
import { BarChart, LineChart } from 'react-native-chart-kit';

export default function Progreso() {
  const data = {
    labels: ["Transporte", "Alimentación", "Energía"],
    datasets: [
      {
        data: [50, 100, 40],
        color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`, // Color personalizado para cada categoría
        strokeWidth: 2
      }
    ]
  };

  return (
    <View>
      <Text style={{ fontSize: 24, textAlign: 'center', margin: 20 }}>Tu Progreso</Text>

      <BarChart
        data={data}
        width={Dimensions.get("window").width - 20}
        height={220}
        yAxisLabel="kg "
        chartConfig={{
          backgroundColor: "#f5f5f5",
          backgroundGradientFrom: "#fff",
          backgroundGradientTo: "#f5f5f5",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 0, 0, ${opacity})`,
          labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
          style: { borderRadius: 16 },
          barPercentage: 0.8,
        }}
        style={{ marginVertical: 8, borderRadius: 16 }}
      />
    </View>
  );
}


- Nuevos Niveles Evolución ( models.py): 

class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # Ejemplo: Oso Polar, Águila, Ballena
    estado = db.Column(db.String(50), nullable=False, default="Inicial")  # Estado del avatar (Inicial, Evolución 1, 2, etc.)
    puntos_necesarios_para_evolucion = db.Column(db.Integer, nullable=False)  # Puntos necesarios para cada evolución


- AVatar fases de evolución en el backend (app.py): 

@app.route('/evolucion_avatar', methods=['POST'])
def evolucionar_avatar():
    data = request.json
    usuario_id = data.get('usuario_id')

    usuario = Usuario.query.get(usuario_id)
    avatar = Avatar.query.filter_by(tipo=usuario.avatar).first()

    if usuario.puntos >= avatar.puntos_necesarios_para_evolucion:
        if avatar.estado == "Inicial":
            avatar.estado = "Evolución 1"
            avatar.puntos_necesarios_para_evolucion = 200  # Para la siguiente evolución
        elif avatar.estado == "Evolución 1":
            avatar.estado = "Evolución 2"
            avatar.puntos_necesarios_para_evolucion = 300
        elif avatar.estado == "Evolución 2":
            avatar.estado = "Evolución 3"  # Última fase

        db.session.commit()
        return jsonify({'message': f'¡Tu {avatar.tipo} ha evolucionado a {avatar.estado}!', 'estado': avatar.estado})
    else:
        return jsonify({'message': 'Aún no tienes suficientes puntos para evolucionar.'})


- Mostrar diferentes evoluciones del avatar en el frontend (AvatarAnimado.js): 

import React, { useState, useEffect } from 'react';
import { View, Text } from 'react-native';
import LottieView from 'lottie-react-native';
import axios from 'axios';

export default function AvatarAnimado({ avatar }) {
  const [estado, setEstado] = useState('Inicial');

  useEffect(() => {
    const obtenerEstadoAvatar = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/evolucion_avatar', { usuario_id: 1 });
        setEstado(response.data.estado);
      } catch (error) {
        console.error('Error al obtener el estado del avatar', error);
      }
    };
    obtenerEstadoAvatar();
  }, [estado]);

  return (
    <View style={{ alignItems: 'center' }}>
      <Text>Tu Avatar: {avatar} - Estado: {estado}</Text>
      <LottieView
        source={require('../assets/animations/' + avatar + '-' + estado + '.json')}  // Ruta de la animación según estado
        autoPlay
        loop
        style={{ width: 150, height: 150 }}
      />
    </View>
  );
}


- Logos y sus Tipos: (models.py)

class Logro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ejemplo: Tiempo, Misiones, Evolución
    puntos_necesarios = db.Column(db.Integer, nullable=False)
    recompensa = db.Column(db.String(255), nullable=False)  # Podría ser una medalla o evolución de avatar

- Actualizar Logros (Logros.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import axios from 'axios';

export default function Logros() {
  const [logros, setLogros] = useState([]);

  useEffect(() => {
    const obtenerLogros = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/logros');
        setLogros(response.data);
      } catch (error) {
        console.error('Error al obtener los logros', error);
      }
    };
    obtenerLogros();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Logros Disponibles</Text>
      <FlatList
        data={logros}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.logro}>
            <Text style={styles.descripcion}>{item.descripcion} ({item.tipo})</Text>
            <Text style={styles.puntos}>Puntos necesarios: {item.puntos_necesarios}</Text>
            <Text style={styles.recompensa}>Recompensa: {item.recompensa}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  logro: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  descripcion: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  puntos: {
    fontSize: 16,
    marginVertical: 5,
  },
  recompensa: {
    fontSize: 16,
    color: '#2e7d32',
  },
});


- Optimización Rendimiento Avatar: (AvatarAnimado.js)

import React, { useState, useEffect } from 'react';
import { View, Text } from 'react-native';
import LottieView from 'lottie-react-native';
import axios from 'axios';

export default function AvatarAnimado({ avatar }) {
  const [estado, setEstado] = useState('Inicial');
  const [animationLoaded, setAnimationLoaded] = useState(false);

  useEffect(() => {
    const obtenerEstadoAvatar = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/evolucion_avatar', { usuario_id: 1 });
        setEstado(response.data.estado);
        setAnimationLoaded(true);  // Solo cargar la animación cuando sea necesario
      } catch (error) {
        console.error('Error al obtener el estado del avatar', error);
      }
    };
    obtenerEstadoAvatar();
  }, [estado]);

  return (
    <View style={{ alignItems: 'center' }}>
      <Text>Tu Avatar: {avatar} - Estado: {estado}</Text>
      {animationLoaded && (
        <LottieView
          source={require('../assets/animations/' + avatar + '-' + estado + '.json')}
          autoPlay
          loop
          style={{ width: 150, height: 150 }}
        />
      )}
    </View>
  );
}


- Carga de rendimiento de graficos (Progreso.js):

import React, { useState, useEffect } from 'react';
import { View, Text, ActivityIndicator, Dimensions } from 'react-native';
import { BarChart } from 'react-native-chart-kit';
import axios from 'axios';

export default function Progreso() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({
    labels: ["Transporte", "Alimentación", "Energía"],
    datasets: [
      { data: [0, 0, 0] }
    ]
  });

  useEffect(() => {
    const obtenerDatosProgreso = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/progreso');
        setData({
          labels: ["Transporte", "Alimentación", "Energía"],
          datasets: [{ data: response.data }]
        });
        setLoading(false);  // Datos cargados
      } catch (error) {
        console.error('Error al obtener los datos de progreso', error);
      }
    };
    obtenerDatosProgreso();
  }, []);

  return (
    <View>
      <Text style={{ fontSize: 24, textAlign: 'center', margin: 20 }}>Tu Progreso</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <BarChart
          data={data}
          width={Dimensions.get("window").width - 20}
          height={220}
          chartConfig={{
            backgroundColor: "#e26a00",
            backgroundGradientFrom: "#fb8c00",
            backgroundGradientTo: "#ffa726",
            decimalPlaces: 2,
            color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
          }}
          style={{ marginVertical: 8, borderRadius: 16 }}
        />
      )}
    </View>
  );
}


-Logros personalizados Backend (app.py): 

@app.route('/logros_personalizados', methods=['GET'])
def logros_personalizados():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    logros = []

    # Logros basados en el uso de transporte
    if usuario.transporte_reducido > 100:  # Ejemplo
        logros.append({
            'descripcion': 'Reducción de transporte',
            'puntos_necesarios': 50,
            'recompensa': 'Medalla de Transporte'
        })

    # Logros basados en la alimentación
    if usuario.dias_alimentacion_sostenible >= 7:  # Ejemplo
        logros.append({
            'descripcion': 'Alimentación Sostenible',
            'puntos_necesarios': 100,
            'recompensa': 'Medalla de Alimentación'
        })

    return jsonify(logros)

- Logos personalizados Frontend (Logros.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import axios from 'axios';

export default function Logros() {
  const [logros, setLogros] = useState([]);

  useEffect(() => {
    const obtenerLogrosPersonalizados = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/logros_personalizados', {
          params: { usuario_id: 1 }  // Simulación del usuario actual
        });
        setLogros(response.data);
      } catch (error) {
        console.error('Error al obtener los logros personalizados', error);
      }
    };
    obtenerLogrosPersonalizados();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Logros Personalizados</Text>
      <FlatList
        data={logros}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.logro}>
            <Text style={styles.descripcion}>{item.descripcion}</Text>
            <Text style={styles.puntos}>Puntos necesarios: {item.puntos_necesarios}</Text>
            <Text style={styles.recompensa}>Recompensa: {item.recompensa}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  logro: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  descripcion: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  puntos: {
    fontSize: 16,
    marginVertical: 5,
  },
  recompensa: {
    fontSize: 16,
    color: '#2e7d32',
  },
});


- Retos globales (models.py): 

class RetoGlobal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    objetivo = db.Column(db.Float, nullable=False)  # Objetivo en kg de CO₂
    progreso_actual = db.Column(db.Float, default=0)  # Progreso acumulado por los usuarios
    fecha_limite = db.Column(db.DateTime, nullable=False)


- Ruta backend (app.py): 

from datetime import datetime

@app.route('/retos_globales', methods=['GET'])
def obtener_retos_globales():
    retos = RetoGlobal.query.all()
    lista_retos = [{
        'descripcion': reto.descripcion,
        'objetivo': reto.objetivo,
        'progreso_actual': reto.progreso_actual,
        'fecha_limite': reto.fecha_limite.strftime("%Y-%m-%d")
    } for reto in retos]
    return jsonify(lista_retos)

@app.route('/unirse_reto_global', methods=['POST'])
def unirse_reto_global():
    data = request.json
    usuario_id = data.get('usuario_id')
    reto_id = data.get('reto_id')
    contribucion = data.get('contribucion')

    reto = RetoGlobal.query.get(reto_id)
    if reto:
        reto.progreso_actual += contribucion
        db.session.commit()
        return jsonify({'message': '¡Contribución añadida!', 'progreso_actual': reto.progreso_actual})
    else:
        return jsonify({'message': 'Reto no encontrado.'}), 404


- Reto globales Frontend (RetosGlobales.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

export default function RetosGlobales() {
  const [retos, setRetos] = useState([]);

  useEffect(() => {
    const obtenerRetosGlobales = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_globales');
        setRetos(response.data);
      } catch (error) {
        console.error('Error al obtener los retos globales', error);
      }
    };
    obtenerRetosGlobales();
  }, []);

  const unirseReto = async (reto_id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/unirse_reto_global', {
        usuario_id: 1,  // Simulación del usuario actual
        reto_id: reto_id,
        contribucion: 10  // Simulación de la contribución en kg de CO₂
      });
      Alert.alert("¡Contribución realizada!", response.data.message);
    } catch (error) {
      console.error('Error al unirse al reto global', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Retos Globales</Text>
      <FlatList
        data={retos}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.reto}>
            <Text>{item.descripcion}</Text>
            <Text>Objetivo: {item.objetivo} kg CO₂</Text>
            <Text>Progreso Actual: {item.progreso_actual} kg CO₂</Text>
            <Text>Fecha Límite: {item.fecha_limite}</Text>
            <Button title="Unirse al Reto" onPress={() => unirseReto(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  reto: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Añadimos Retos Globales en Navigator (MainNavigator.js): 

import RetosGlobales from '../screens/RetosGlobales';

export default function MainNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SeleccionAvatar">
        <Stack.Screen name="SeleccionAvatar" component={SeleccionAvatar} options={{ title: 'Selecciona tu Avatar' }} />
        <Stack.Screen name="HuellaCarbono" component={HuellaCarbono} options={{ title: 'Huella de Carbono' }} />
        <Stack.Screen name="Misiones" component={Misiones} options={{ title: 'Misiones Diarias' }} />
        <Stack.Screen name="Progreso" component={Progreso} options={{ title: 'Progreso' }} />
        <Stack.Screen name="Logros" component={Logros} options={{ title: 'Logros Disponibles' }} />
        <Stack.Screen name="RetosGlobales" component={RetosGlobales} options={{ title: 'Retos Globales' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


- Progreso Reto globales (RetosGlobales.js): 

import { ProgressBar } from 'react-native-paper';  // Importamos la barra de progreso

export default function RetosGlobales() {
  // Resto del código...

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Retos Globales</Text>
      <FlatList
        data={retos}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.reto}>
            <Text>{item.descripcion}</Text>
            <Text>Objetivo: {item.objetivo} kg CO₂</Text>
            <Text>Progreso Actual: {item.progreso_actual} kg CO₂</Text>
            <Text>Fecha Límite: {item.fecha_limite}</Text>
            <ProgressBar progress={item.progreso_actual / item.objetivo} color="#4caf50" style={{ height: 10, marginTop: 10 }} />
            <Button title="Unirse al Reto" onPress={() => unirseReto(item.id)} />
          </View>
        )}
      />
    </View>
  );
}


- Tabla de classificación (app.py): 

@app.route('/clasificaciones', methods=['GET'])
def obtener_clasificaciones():
    usuarios = Usuario.query.order_by(Usuario.puntos.desc()).limit(10).all()
    lista_usuarios = [{'nombre': usuario.nombre, 'puntos': usuario.puntos} for usuario in usuarios]
    return jsonify(lista_usuarios)


- Mostrar Classificacion Frontend (Clasificaciones.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

export default function Clasificaciones() {
  const [clasificaciones, setClasificaciones] = useState([]);

  useEffect(() => {
    const obtenerClasificaciones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/clasificaciones');
        setClasificaciones(response.data);
      } catch (error) {
        console.error('Error al obtener las clasificaciones', error);
      }
    };
    obtenerClasificaciones();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Clasificaciones</Text>
      <FlatList
        data={clasificaciones}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.clasificacion}>
            <Text>{item.nombre} - {item.puntos} puntos</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  clasificacion: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Añadir classificacion a NAvigator (MainNavigator.js): 

import Clasificaciones from '../screens/Clasificaciones';

export default function MainNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SeleccionAvatar">
        {/* Otras pantallas */}
        <Stack.Screen name="Clasificaciones" component={Clasificaciones} options={{ title: 'Clasificaciones' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


- Notificaciones en timepo real (Backend con WebSockets (Flask-SocketIO)): 

pip install flask-socketio
pip install eventlet  # Recomendado para el uso de WebSockets con Flask

- Configuarr servidor con flask: (app.py)

from flask_socketio import SocketIO, emit
import eventlet

socketio = SocketIO(app, cors_allowed_origins="*")

# Evento para notificar sobre contribuciones a retos globales
@socketio.on('unirse_reto_global')
def handle_reto_global(data):
    usuario_id = data.get('usuario_id')
    reto_id = data.get('reto_id')
    contribucion = data.get('contribucion')

    reto = RetoGlobal.query.get(reto_id)
    if reto:
        reto.progreso_actual += contribucion
        db.session.commit()

        # Emitir notificación a todos los usuarios conectados
        emit('actualizacion_reto_global', {
            'reto_id': reto.id,
            'descripcion': reto.descripcion,
            'progreso_actual': reto.progreso_actual,
            'objetivo': reto.objetivo
        }, broadcast=True)

        return {'message': 'Contribución añadida y notificación enviada.'}
    else:
        return {'message': 'Reto no encontrado.'}, 404

if __name__ == "__main__":
    socketio.run(app)


- Frontend Socket notificaciones: 
npm install socket.io-client

- Conxeion WebSocket (RetosGlobales.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Alert } from 'react-native';
import io from 'socket.io-client';
import axios from 'axios';

const socket = io("http://127.0.0.1:5000");

export default function RetosGlobales() {
  const [retos, setRetos] = useState([]);

  useEffect(() => {
    const obtenerRetosGlobales = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_globales');
        setRetos(response.data);
      } catch (error) {
        console.error('Error al obtener los retos globales', error);
      }
    };
    obtenerRetosGlobales();

    // Suscribirse a actualizaciones de retos globales en tiempo real
    socket.on('actualizacion_reto_global', (data) => {
      Alert.alert(
        "¡Actualización de Reto Global!",
        `El reto "${data.descripcion}" ha alcanzado ${data.progreso_actual} kg CO₂ de un total de ${data.objetivo} kg CO₂.`
      );
    });

    return () => {
      socket.off('actualizacion_reto_global');
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Retos Globales</Text>
      <FlatList
        data={retos}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.reto}>
            <Text>{item.descripcion}</Text>
            <Text>Objetivo: {item.objetivo} kg CO₂</Text>
            <Text>Progreso Actual: {item.progreso_actual} kg CO₂</Text>
            <Button title="Unirse al Reto" onPress={() => unirseReto(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  reto: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Retos personalizados (models.py): 

class RetoPersonalizado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    creador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    progreso_objetivo = db.Column(db.Float, nullable=False)
    progreso_actual = db.Column(db.Float, default=0)
    fecha_limite = db.Column(db.DateTime, nullable=False)
    participantes = db.relationship('Usuario', secondary='reto_participantes', backref='retos_personalizados')

# Relación entre retos personalizados y los participantes
reto_participantes = db.Table('reto_participantes',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('reto_id', db.Integer, db.ForeignKey('reto_personalizado.id'))
)

- Ruta ret personalizado (app.py): 

@app.route('/crear_reto_personalizado', methods=['POST'])
def crear_reto_personalizado():
    data = request.json
    descripcion = data.get('descripcion')
    creador_id = data.get('creador_id')
    progreso_objetivo = data.get('progreso_objetivo')
    fecha_limite = datetime.strptime(data.get('fecha_limite'), '%Y-%m-%d')

    nuevo_reto = RetoPersonalizado(
        descripcion=descripcion,
        creador_id=creador_id,
        progreso_objetivo=progreso_objetivo,
        fecha_limite=fecha_limite
    )
    db.session.add(nuevo_reto)
    db.session.commit()

    return jsonify({'message': 'Reto personalizado creado con éxito.'})

@app.route('/unirse_reto_personalizado', methods=['POST'])
def unirse_reto_personalizado():
    data = request.json
    usuario_id = data.get('usuario_id')
    reto_id = data.get('reto_id')

    reto = RetoPersonalizado.query.get(reto_id)
    usuario = Usuario.query.get(usuario_id)
    reto.participantes.append(usuario)
    db.session.commit()

    return jsonify({'message': 'Te has unido al reto personalizado.'})

- Retos personalizados Fronted (RetosPersonalizados.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, TextInput } from 'react-native';
import axios from 'axios';

export default function RetosPersonalizados() {
  const [retos, setRetos] = useState([]);
  const [descripcion, setDescripcion] = useState('');
  const [progresoObjetivo, setProgresoObjetivo] = useState('');
  const [fechaLimite, setFechaLimite] = useState('');

  useEffect(() => {
    const obtenerRetosPersonalizados = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_personalizados');
        setRetos(response.data);
      } catch (error) {
        console.error('Error al obtener los retos personalizados', error);
      }
    };
    obtenerRetosPersonalizados();
  }, []);

  const crearReto = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/crear_reto_personalizado', {
        descripcion,
        creador_id: 1,  // Usuario actual
        progreso_objetivo: parseFloat(progresoObjetivo),
        fecha_limite: fechaLimite
      });
      alert('Reto creado con éxito');
    } catch (error) {
      console.error('Error al crear el reto personalizado', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Retos Personalizados</Text>
      <FlatList
        data={retos}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.reto}>
            <Text>{item.descripcion}</Text>
            <Text>Objetivo: {item.progreso_objetivo} kg CO₂</Text>
            <Text>Fecha Límite: {item.fecha_limite}</Text>
            <Button title="Unirse al Reto" onPress={() => unirseReto(item.id)} />
          </View>
        )}
      />

      <View style={styles.form}>
        <TextInput
          placeholder="Descripción del Reto"
          value={descripcion}
          onChangeText={setDescripcion}
          style={styles.input}
        />
        <TextInput
          placeholder="Objetivo en kg CO₂"
          value={progresoObjetivo}
          onChangeText={setProgresoObjetivo}
          keyboardType="numeric"
          style={styles.input}
        />
        <TextInput
          placeholder="Fecha Límite (YYYY-MM-DD)"
          value={fechaLimite}
          onChangeText={setFechaLimite}
          style={styles.input}
        />
        <Button title="Crear Reto" onPress={crearReto} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  reto: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  form: {
    marginTop: 20,
  },
  input: {
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
});



-Acccesorios Avatar (models.py): 

class AccesorioAvatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ejemplo: sombrero, gafas, etc.
    puntos_necesarios = db.Column(db.Integer, nullable=False)  # Puntos necesarios para desbloquear
    imagen_url = db.Column(db.String(255), nullable=False)  # URL o ruta de la imagen del accesorio


- Desbloquear accesorios (app.py): 

@app.route('/desbloquear_accesorio', methods=['POST'])
def desbloquear_accesorio():
    data = request.json
    usuario_id = data.get('usuario_id')
    accesorio_id = data.get('accesorio_id')

    accesorio = AccesorioAvatar.query.get(accesorio_id)
    usuario = Usuario.query.get(usuario_id)

    if usuario.puntos >= accesorio.puntos_necesarios:
        usuario.accesorios.append(accesorio)  # Asignar el accesorio al usuario
        db.session.commit()
        return jsonify({'message': f'¡Has desbloqueado {accesorio.nombre} para tu avatar!'})
    else:
        return jsonify({'message': 'No tienes suficientes puntos para desbloquear este accesorio.'}), 400


-Aplicar accesorios (AvatarCustomization.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Image, Alert } from 'react-native';
import axios from 'axios';

export default function AvatarCustomization() {
  const [accesorios, setAccesorios] = useState([]);
  const [avatarActual, setAvatarActual] = useState({
    accesorios_aplicados: []
  });

  useEffect(() => {
    const obtenerAccesorios = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/accesorios_usuario', { params: { usuario_id: 1 } });
        setAccesorios(response.data);
      } catch (error) {
        console.error('Error al obtener los accesorios', error);
      }
    };

    obtenerAccesorios();
  }, []);

  const aplicarAccesorio = async (accesorio_id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/aplicar_accesorio', {
        usuario_id: 1,  // Simulación del usuario actual
        accesorio_id
      });
      Alert.alert("¡Accesorio aplicado!", response.data.message);
      setAvatarActual({ ...avatarActual, accesorios_aplicados: [...avatarActual.accesorios_aplicados, accesorio_id] });
    } catch (error) {
      console.error('Error al aplicar el accesorio', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Personalización del Avatar</Text>
      <FlatList
        data={accesorios}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.accesorio}>
            <Image source={{ uri: item.imagen_url }} style={styles.imagenAccesorio} />
            <Text>{item.nombre}</Text>
            <Button title="Aplicar" onPress={() => aplicarAccesorio(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  accesorio: {
    marginBottom: 20,
    alignItems: 'center',
  },
  imagenAccesorio: {
    width: 100,
    height: 100,
    marginBottom: 10,
  },
});


-Aplicar avatar accesorios (AvatarAnimado.js): 

import React from 'react';
import { View, Text, Image } from 'react-native';
import LottieView from 'lottie-react-native';

export default function AvatarAnimado({ avatar, accesorios }) {
  return (
    <View style={{ alignItems: 'center' }}>
      <LottieView
        source={require('../assets/animations/' + avatar + '.json')}
        autoPlay
        loop
        style={{ width: 150, height: 150 }}
      />

      {/* Mostrar los accesorios aplicados */}
      {accesorios.map(accesorio => (
        <Image key={accesorio.id} source={{ uri: accesorio.imagen_url }} style={{ position: 'absolute', width: 50, height: 50 }} />
      ))}
    </View>
  );
}


- Rachas Backend (models.py):

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    puntos = db.Column(db.Integer, default=0)
    racha_dias = db.Column(db.Integer, default=0)  # Racha de días consecutivos
    ultima_entrada = db.Column(db.DateTime)


- Actalizar rachas (app.py)

@app.route('/actualizar_racha', methods=['POST'])
def actualizar_racha():
    usuario_id = request.json.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    hoy = datetime.utcnow().date()
    ultima_entrada = usuario.ultima_entrada.date() if usuario.ultima_entrada else None

    if ultima_entrada == hoy:
        return jsonify({'message': 'Ya has iniciado sesión hoy.'})

    if ultima_entrada and (hoy - ultima_entrada).days == 1:
        usuario.racha_dias += 1
    else:
        usuario.racha_dias = 1

    usuario.ultima_entrada = datetime.utcnow()
    db.session.commit()

    recompensa = usuario.racha_dias * 10  # Ejemplo: 10 puntos por día consecutivo
    usuario.puntos += recompensa
    db.session.commit()

    return jsonify({'message': f'Has mantenido una racha de {usuario.racha_dias} días y has ganado {recompensa} puntos.'}

  - Mostar rachas frontend (RachasDiarias.js)

import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';
import axios from 'axios';

export default function RachasDiarias() {
  const [rachaDias, setRachaDias] = useState(0);
  const [puntosGanados, setPuntosGanados] = useState(0);

  useEffect(() => {
    const actualizarRacha = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/actualizar_racha', { usuario_id: 1 });
        setRachaDias(response.data.racha_dias);
        setPuntosGanados(response.data.recompensa);
        Alert.alert('Recompensa diaria', response.data.message);
      } catch (error) {
        console.error('Error al actualizar la racha', error);
      }
    };

    actualizarRacha();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Recompensas Diarias</Text>
      <Text style={styles.text}>Racha de Días: {rachaDias}</Text>
      <Text style={styles.text}>Puntos Ganados Hoy: {puntosGanados}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  text: {
    fontSize: 18,
    textAlign: 'center',
  },
});


- Niveles backend (app.py): 

@app.route('/nivel_usuario', methods=['GET'])
def nivel_usuario():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    niveles = [0, 100, 250, 500, 1000]  # Ejemplo de niveles
    nivel_actual = next((i for i, puntos in enumerate(niveles) if usuario.puntos < puntos), len(niveles))

    return jsonify({'nivel': nivel_actual, 'puntos': usuario.puntos})


- Mostrar niveles forntend (NivelesUsuario.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import axios from 'axios';

export default function NivelesUsuario() {
  const [nivel, setNivel] = useState(1);
  const [puntos, setPuntos] = useState(0);

  useEffect(() => {
    const obtenerNivel = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/nivel_usuario', { params: { usuario_id: 1 } });
        setNivel(response.data.nivel);
        setPuntos(response.data.puntos);
      } catch (error) {
        console.error('Error al obtener el nivel del usuario', error);
      }
    };

    obtenerNivel();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tu Nivel</Text>
      <Text style={styles.text}>Nivel: {nivel}</Text>
      <Text style={styles.text}>Puntos: {puntos}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  text: {
    fontSize: 18,
    textAlign: 'center',
  },
});


- Accesorios amplios (models.py): 

class AccesorioAvatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ejemplo: ropa, fondo, color
    puntos_necesarios = db.Column(db.Integer, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=False)


- Categorias personalizacion (app.py): 

@app.route('/accesorios', methods=['GET'])
def obtener_accesorios():
    tipo = request.args.get('tipo')
    accesorios = AccesorioAvatar.query.filter_by(tipo=tipo).all()
    lista_accesorios = [{'id': accesorio.id, 'nombre': accesorio.nombre, 'imagen_url': accesorio.imagen_url, 'puntos_necesarios': accesorio.puntos_necesarios} for accesorio in accesorios]
    return jsonify(lista_accesorios)


- Pantalla personalizacion (AvatarCustomization.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Image, Alert } from 'react-native';
import axios from 'axios';

export default function AvatarCustomization() {
  const [accesorios, setAccesorios] = useState([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState('ropa');

  useEffect(() => {
    const obtenerAccesorios = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/accesorios', {
          params: { tipo: categoriaSeleccionada }
        });
        setAccesorios(response.data);
      } catch (error) {
        console.error('Error al obtener los accesorios', error);
      }
    };

    obtenerAccesorios();
  }, [categoriaSeleccionada]);

  const aplicarAccesorio = async (accesorio_id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/aplicar_accesorio', {
        usuario_id: 1,  // Simulación del usuario actual
        accesorio_id
      });
      Alert.alert("¡Accesorio aplicado!", response.data.message);
    } catch (error) {
      console.error('Error al aplicar el accesorio', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Personaliza tu Avatar</Text>

      {/* Botones para cambiar de categoría */}
      <View style={styles.categorias}>
        <Button title="Ropa" onPress={() => setCategoriaSeleccionada('ropa')} />
        <Button title="Fondos" onPress={() => setCategoriaSeleccionada('fondo')} />
        <Button title="Colores" onPress={() => setCategoriaSeleccionada('color')} />
      </View>

      <FlatList
        data={accesorios}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.accesorio}>
            <Image source={{ uri: item.imagen_url }} style={styles.imagenAccesorio} />
            <Text>{item.nombre}</Text>
            <Button title="Aplicar" onPress={() => aplicarAccesorio(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  categorias: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
  accesorio: {
    marginBottom: 20,
    alignItems: 'center',
  },
  imagenAccesorio: {
    width: 100,
    height: 100,
    marginBottom: 10,
  },
});


- EFectos visaules dinamicos (AvatarAnimado.js)

import React from 'react';
import { View, Image } from 'react-native';
import LottieView from 'lottie-react-native';

export default function AvatarAnimado({ avatar, accesorios, efectos }) {
  return (
    <View style={{ alignItems: 'center' }}>
      <LottieView
        source={require('../assets/animations/' + avatar + '.json')}
        autoPlay
        loop
        style={{ width: 150, height: 150 }}
      />

      {/* Mostrar los accesorios aplicados */}
      {accesorios.map(accesorio => (
        <Image key={accesorio.id} source={{ uri: accesorio.imagen_url }} style={{ position: 'absolute', width: 50, height: 50 }} />
      ))}

      {/* Mostrar los efectos visuales */}
      {efectos && <LottieView source={require('../assets/animations/efecto-luz.json')} autoPlay loop style={{ width: 200, height: 200, position: 'absolute' }} />}
    </View>
  );
}


-Logros especiales (app.py)

@app.route('/logros_especiales', methods=['GET'])
def obtener_logros_especiales():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    logros = []

    # Ejemplo: Logro por completar 50 misiones
    if usuario.misiones_completadas >= 50:
        logros.append({
            'descripcion': 'Misión Cumplida',
            'recompensa': 'Medalla de Oro'
        })

    # Ejemplo: Logro por mantener una racha de 30 días
    if usuario.racha_dias >= 30:
        logros.append({
            'descripcion': 'Racha de Campeón',
            'recompensa': 'Medalla de Platino'
        })

    return jsonify(logros)


- Mostrado logos epseciales frontend (LogrosEspeciales.js):

import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

export default function LogrosEspeciales() {
  const [logros, setLogros] = useState([]);

  useEffect(() => {
    const obtenerLogrosEspeciales = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/logros_especiales', {
          params: { usuario_id: 1 }  // Simulación del usuario actual
        });
        setLogros(response.data);
      } catch (error) {
        console.error('Error al obtener los logros especiales', error);
      }
    };

    obtenerLogrosEspeciales();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tus Logros Especiales</Text>
      <FlatList
        data={logros}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.logro}>
            <Text>{item.descripcion}</Text>
            <Text>Recompensa: {item.recompensa}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  logro: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Efectos especiales para logros (LogroDesbloqueado.js): 

import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import LottieView from 'lottie-react-native';

export default function LogroDesbloqueado({ route }) {
  const { logro } = route.params;

  useEffect(() => {
    // Mostrar animación cuando se carga la pantalla
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>¡Logro Desbloqueado!</Text>
      <Text style={styles.logroDescripcion}>{logro.descripcion}</Text>
      <LottieView
        source={require('../assets/animations/fuegos-artificiales.json')}
        autoPlay
        loop={false}
        style={{ width: 300, height: 300 }}
      />
      <Text style={styles.recompensa}>Recompensa: {logro.recompensa}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  logroDescripcion: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  recompensa: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 20,
  },
});


-Fondos animados backend (models.py): 

class AccesorioAvatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ahora puede ser 'ropa', 'fondo', 'color', etc.
    puntos_necesarios = db.Column(db.Integer, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=False)  # Para fondos animados, aquí se almacena la URL


- Aplicamos fondos en (app.py): 

@app.route('/fondos', methods=['GET'])
def obtener_fondos():
    fondos = AccesorioAvatar.query.filter_by(tipo='fondo').all()
    lista_fondos = [{'id': fondo.id, 'nombre': fondo.nombre, 'imagen_url': fondo.imagen_url, 'puntos_necesarios': fondo.puntos_necesarios} for fondo in fondos]
    return jsonify(lista_fondos)

@app.route('/aplicar_fondo', methods=['POST'])
def aplicar_fondo():
    data = request.json
    usuario_id = data.get('usuario_id')
    fondo_id = data.get('fondo_id')

    fondo = AccesorioAvatar.query.get(fondo_id)
    usuario = Usuario.query.get(usuario_id)

    if usuario.puntos >= fondo.puntos_necesarios:
        usuario.fondo_actual = fondo.imagen_url  # Actualizamos el fondo actual del usuario
        db.session.commit()
        return jsonify({'message': 'Fondo aplicado con éxito.'})
    else:
        return jsonify({'message': 'No tienes suficientes puntos para aplicar este fondo.'}), 400


- Visualizacion de los fondos en forntend: (Fondos.js)

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Image, Alert } from 'react-native';
import axios from 'axios';

export default function Fondos() {
  const [fondos, setFondos] = useState([]);

  useEffect(() => {
    const obtenerFondos = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/fondos');
        setFondos(response.data);
      } catch (error) {
        console.error('Error al obtener los fondos', error);
      }
    };

    obtenerFondos();
  }, []);

  const aplicarFondo = async (fondo_id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/aplicar_fondo', {
        usuario_id: 1,  // Usuario actual
        fondo_id
      });
      Alert.alert("¡Fondo aplicado!", response.data.message);
    } catch (error) {
      console.error('Error al aplicar el fondo', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Selecciona tu Fondo Animado</Text>
      <FlatList
        data={fondos}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.fondo}>
            <Image source={{ uri: item.imagen_url }} style={styles.imagenFondo} />
            <Text>{item.nombre}</Text>
            <Button title="Aplicar" onPress={() => aplicarFondo(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  fondo: {
    marginBottom: 20,
    alignItems: 'center',
  },
  imagenFondo: {
    width: 200,
    height: 150,
    marginBottom: 10,
  },
});


- Aplicar fondo al avatar (AvatarAnimado.js): 

import React from 'react';
import { View, ImageBackground } from 'react-native';
import LottieView from 'lottie-react-native';

export default function AvatarAnimado({ avatar, fondo, accesorios }) {
  return (
    <ImageBackground source={{ uri: fondo }} style={{ width: 300, height: 300 }}>
      <LottieView
        source={require('../assets/animations/' + avatar + '.json')}
        autoPlay
        loop
        style={{ width: 150, height: 150, alignSelf: 'center' }}
      />
      {/* Mostrar los accesorios aplicados */}
      {accesorios.map(accesorio => (
        <Image key={accesorio.id} source={{ uri: accesorio.imagen_url }} style={{ position: 'absolute', width: 50, height: 50 }} />
      ))}
    </ImageBackground>
  );
}


- Tienda Virtsual Backend (app.py): 

@app.route('/tienda', methods=['GET'])
def obtener_items_tienda():
    items = AccesorioAvatar.query.all()
    lista_items = [{'id': item.id, 'nombre': item.nombre, 'tipo': item.tipo, 'puntos_necesarios': item.puntos_necesarios, 'imagen_url': item.imagen_url} for item in items]
    return jsonify(lista_items)

-Comprar items backend (app.py): 

@app.route('/comprar_item', methods=['POST'])
def comprar_item():
    data = request.json
    usuario_id = data.get('usuario_id')
    item_id = data.get('item_id')

    usuario = Usuario.query.get(usuario_id)
    item = AccesorioAvatar.query.get(item_id)

    if usuario.puntos >= item.puntos_necesarios:
        usuario.puntos -= item.puntos_necesarios
        usuario.accesorios.append(item)  # Asignar el ítem al usuario
        db.session.commit()
        return jsonify({'message': f'¡Has comprado {item.nombre}!', 'puntos_restantes': usuario.puntos})
    else:
        return jsonify({'message': 'No tienes suficientes puntos para este ítem.'}), 400


- Pantalla tienda frontend (Tienda.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Image, Alert } from 'react-native';
import axios from 'axios';

export default function Tienda() {
  const [items, setItems] = useState([]);
  const [puntosUsuario, setPuntosUsuario] = useState(0);

  useEffect(() => {
    const obtenerItemsTienda = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/tienda');
        setItems(response.data);
        const usuarioResponse = await axios.get('http://127.0.0.1:5000/usuario', { params: { usuario_id: 1 } });
        setPuntosUsuario(usuarioResponse.data.puntos);
      } catch (error) {
        console.error('Error al obtener los items de la tienda', error);
      }
    };

    obtenerItemsTienda();
  }, []);

  const comprarItem = async (item_id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/comprar_item', {
        usuario_id: 1,  // Usuario actual
        item_id
      });
      Alert.alert("¡Compra realizada!", response.data.message);
      setPuntosUsuario(response.data.puntos_restantes);
    } catch (error) {
      console.error('Error al comprar el ítem', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tienda</Text>
      <Text style={styles.puntos}>Puntos: {puntosUsuario}</Text>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Image source={{ uri: item.imagen_url }} style={styles.imagenItem} />
            <Text>{item.nombre}</Text>
            <Text>Puntos necesarios: {item.puntos_necesarios}</Text>
            <Button title="Comprar" onPress={() => comprarItem(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1, 
    padding: 20, 
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  puntos: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  item: {
    marginBottom: 20,
    alignItems: 'center',
  },
  imagenItem: {
    width: 100,
    height: 100,
    marginBottom: 10,
  },
});


- Logros y recompensas Backend (app.py): 

@app.route('/logros_retos_globales', methods=['POST'])
def logros_retos_globales():
    data = request.json
    usuario_id = data.get('usuario_id')
    reto_id = data.get('reto_id')
    contribucion = data.get('contribucion')

    reto = RetoGlobal.query.get(reto_id)
    usuario = Usuario.query.get(usuario_id)

    if contribucion >= 100:  # Ejemplo: contribución significativa
        usuario.logros.append('Contribuidor Global')
        db.session.commit()
        return jsonify({'message': '¡Has ganado el logro Contribuidor Global!'})
    else:
        return jsonify({'message': 'Contribución registrada, sigue participando.'})


- Logros por colecciones de accesorios (Backend / app.py): 

@app.route('/logros_colecciones', methods=['GET'])
def logros_colecciones():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    coleccion_ropa = ['Sombrero', 'Camiseta', 'Pantalones']
    accesorios_usuario = [a.nombre for a in usuario.accesorios]

    if all(item in accesorios_usuario for item in coleccion_ropa):
        usuario.logros.append('Colección Completa: Ropa')
        db.session.commit()
        return jsonify({'message': '¡Has completado la colección de ropa!'})
    else:
        return jsonify({'message': 'Aún no has completado la colección.'})


- Ranking backend (app.js): 

@app.route('/clasificaciones', methods=['GET'])
def obtener_clasificaciones():
    usuarios = Usuario.query.order_by(Usuario.puntos.desc()).limit(10).all()
    clasificaciones = [{'nombre': usuario.nombre, 'puntos': usuario.puntos} for usuario in usuarios]
    return jsonify(clasificaciones)


- Ranking Frontend (Clasificacciones.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

export default function Clasificaciones() {
  const [clasificaciones, setClasificaciones] = useState([]);

  useEffect(() => {
    const obtenerClasificaciones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/clasificaciones');
        setClasificaciones(response.data);
      } catch (error) {
        console.error('Error al obtener las clasificaciones', error);
      }
    };

    obtenerClasificaciones();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Clasificación Global</Text>
      <FlatList
        data={clasificaciones}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item, index }) => (
          <View style={styles.clasificacion}>
            <Text>{index + 1}. {item.nombre} - {item.puntos} puntos</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  clasificacion: {
    padding: 15,
    marginBottom: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Ranking tipos (app.py) (Backend): 

@app.route('/clasificaciones_huella', methods=['GET'])
def obtener_clasificaciones_huella():
    usuarios = Usuario.query.order_by(Usuario.huella_reducida.desc()).limit(10).all()
    clasificaciones = [{'nombre': usuario.nombre, 'huella_reducida': usuario.huella_reducida} for usuario in usuarios]
    return jsonify(clasificaciones)



- Retos temporales Backend (models.py): 

class RetoSemanal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    ganador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))  # Ganador del reto
    progreso = db.relationship('ProgresoReto', backref='reto_semanal')

class ProgresoReto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    reto_id = db.Column(db.Integer, db.ForeignKey('reto_semanal.id'))
    progreso_actual = db.Column(db.Float, nullable=False)


- Unir y paricpar reto semanal (Backend) (app.py): 

@app.route('/unirse_reto_semanal', methods=['POST'])
def unirse_reto_semanal():
    data = request.json
    usuario_id = data.get('usuario_id')
    reto_id = data.get('reto_id')

    reto = RetoSemanal.query.get(reto_id)
    usuario = Usuario.query.get(usuario_id)

    progreso = ProgresoReto(usuario_id=usuario_id, reto_id=reto_id, progreso_actual=0)
    db.session.add(progreso)
    db.session.commit()

    return jsonify({'message': 'Te has unido al reto semanal.'})

@app.route('/actualizar_progreso_reto', methods=['POST'])
def actualizar_progreso_reto():
    data = request.json
    usuario_id = data.get('usuario_id')
    reto_id = data.get('reto_id')
    progreso_adicional = data.get('progreso')

    progreso = ProgresoReto.query.filter_by(usuario_id=usuario_id, reto_id=reto_id).first()
    progreso.progreso_actual += progreso_adicional
    db.session.commit()

    return jsonify({'message': 'Progreso actualizado.', 'progreso_actual': progreso.progreso_actual})


- Mostrar retos semanales (Frontend) ( RetosSemanales.js)

import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

export default function RetosSemanales() {
  const [retos, setRetos] = useState([]);

  useEffect(() => {
    const obtenerRetosSemanales = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/retos_semanales');
        setRetos(response.data);
      } catch (error) {
        console.error('Error al obtener los retos semanales', error);
      }
    };

    obtenerRetosSemanales();
  }, []);

  const unirseReto = async (reto_id) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/unirse_reto_semanal', {
        usuario_id: 1,  // Usuario actual
        reto_id
      });
      Alert.alert("Te has unido al reto semanal", response.data.message);
    } catch (error) {
      console.error('Error al unirse al reto semanal', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Retos Semanales</Text>
      <FlatList
        data={retos}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.reto}>
            <Text>{item.descripcion}</Text>
            <Button title="Unirse al Reto" onPress={() => unirseReto(item.id)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  reto: {
    marginBottom: 20,
    padding: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Optimización de Lottie (Frontend) (AvatarAnimado.js): 

import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator } from 'react-native';
import LottieView from 'lottie-react-native';

export default function AvatarAnimado({ avatar, fondo }) {
  const [animacionCargada, setAnimacionCargada] = useState(false);

  useEffect(() => {
    const precargarAnimacion = async () => {
      // Simulamos la precarga de la animación
      setTimeout(() => setAnimacionCargada(true), 1000);  // Simula 1 segundo de carga
    };
    precargarAnimacion();
  }, []);

  return (
    <View style={{ alignItems: 'center' }}>
      {animacionCargada ? (
        <LottieView
          source={require('../assets/animations/' + avatar + '.json')}
          autoPlay
          loop
          style={{ width: 150, height: 150 }}
        />
      ) : (
        <ActivityIndicator size="large" color="#0000ff" />
      )}
    </View>
  );
}


- Transicciones entre pantallas Frontend (MainNavigator.js): 

import { createStackNavigator, TransitionPresets } from '@react-navigation/stack';
const Stack = createStackNavigator();

export default function MainNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          ...TransitionPresets.SlideFromRightIOS,  // Ejemplo de transición suave
        }}>
        <Stack.Screen name="Clasificaciones" component={Clasificaciones} />
        <Stack.Screen name="RetosSemanales" component={RetosSemanales} />
        {/* Otras pantallas */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}


- Sociales Backend (models.py):

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reto_id = db.Column(db.Integer, db.ForeignKey('reto_global.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    texto = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


- Backend social (app.py) : 

@app.route('/comentarios_reto', methods=['POST'])
def agregar_comentario_reto():
    data = request.json
    reto_id = data.get('reto_id')
    usuario_id = data.get('usuario_id')
    texto = data.get('texto')

    comentario = Comentario(reto_id=reto_id, usuario_id=usuario_id, texto=texto)
    db.session.add(comentario)
    db.session.commit()

    return jsonify({'message': 'Comentario agregado.'})

@app.route('/comentarios_reto/<int:reto_id>', methods=['GET'])
def obtener_comentarios_reto(reto_id):
    comentarios = Comentario.query.filter_by(reto_id=reto_id).all()
    lista_comentarios = [{'usuario_id': c.usuario_id, 'texto': c.texto, 'fecha': c.fecha} for c in comentarios]
    return jsonify(lista_comentarios)


- Mostrar comentarios forntend (ComentariosReto.js):

import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

export default function ComentariosReto({ reto_id }) {
  const [comentarios, setComentarios] = useState([]);
  const [textoComentario, setTextoComentario] = useState('');

  useEffect(() => {
    const obtenerComentarios = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/comentarios_reto/${reto_id}`);
        setComentarios(response.data);
      } catch (error) {
        console.error('Error al obtener los comentarios', error);
      }
    };

    obtenerComentarios();
  }, []);

  const agregarComentario = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/comentarios_reto', {
        reto_id,
        usuario_id: 1,  // Usuario actual
        texto: textoComentario
      });
      setTextoComentario('');
      // Volver a cargar los comentarios
      const response = await axios.get(`http://127.0.0.1:5000/comentarios_reto/${reto_id}`);
      setComentarios(response.data);
    } catch (error) {
      console.error('Error al agregar comentario', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Comentarios del Reto</Text>
      <FlatList
        data={comentarios}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.comentario}>
            <Text>{item.texto}</Text>
          </View>
        )}
      />
      <TextInput
        value={textoComentario}
        onChangeText={setTextoComentario}
        placeholder="Escribe un comentario..."
        style={styles.input}
      />
      <Button title="Agregar Comentario" onPress={agregarComentario} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  comentario: {
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    marginBottom: 10,
  },
  input: {
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
});




**IA**

-Machine Learning: (models.py) 

class ActividadUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    tipo_actividad = db.Column(db.String(50))  # Ejemplo: transporte, alimentación, energía
    cantidad = db.Column(db.Float)  # Cantidad de la actividad (por ejemplo, km para transporte)
    huella_carbono = db.Column(db.Float)  # Huella de carbono calculada para esa actividad
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


- CSV DATASET: 

usuario_id,tipo_actividad,cantidad,huella_carbono,dia_semana,seguimiento_recomendacion
1,transporte,20,5.4,1,1  # El usuario siguió la recomendación
1,alimentacion,2.5,1.2,1,0  # El usuario no siguió la recomendación
...


- Modelo de recomendaciones: (

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

# Cargar el dataset
data = pd.read_csv('actividades_usuario.csv')

# Definir las características (features) y la variable objetivo (target)
X = data[['tipo_actividad', 'cantidad', 'dia_semana']]  # Características
y = data['huella_carbono']  # Objetivo: huella de carbono

# Convertir variables categóricas a numéricas
X = pd.get_dummies(X, columns=['tipo_actividad', 'dia_semana'])

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo de regresión
modelo = RandomForestRegressor()
modelo.fit(X_train, y_train)

# Evaluar el modelo
score = modelo.score(X_test, y_test)
print(f'Precisión del modelo: {score}')


- Predicciones Backend: 

# Modificamos el objetivo (target) para que sea la huella de carbono futura
# Predicción de huella de carbono a 7 días
data['huella_carbono_futura'] = data['huella_carbono'].shift(-7)  # Usar datos de los próximos 7 días

# Reentrenar el modelo con el nuevo objetivo
y = data['huella_carbono_futura'].dropna()  # Eliminar valores nulos resultantes del shift
X_train, X_test, y_train, y_test = train_test_split(X[:-7], y, test_size=0.2, random_state=42)

# Entrenar y evaluar el modelo
modelo.fit(X_train, y_train)
score = modelo.score(X_test, y_test)
print(f'Precisión del modelo de predicción futura: {score}')


- Mostar Predicciones Frontend (PrediccionFutura.js)

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import axios from 'axios';

export default function PrediccionFutura() {
  const [prediccion, setPrediccion] = useState([]);

  useEffect(() => {
    const obtenerPrediccion = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/prediccion_futura', {
          params: { usuario_id: 1 }  // Simulación del usuario actual
        });
        setPrediccion(response.data);
      } catch (error) {
        console.error('Error al obtener la predicción futura', error);
      }
    };

    obtenerPrediccion();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Predicción de tu Huella de Carbono</Text>
      <FlatList
        data={prediccion}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text>Fecha: {item.fecha}</Text>
            <Text>Huella estimada: {item.huella_carbono_estimada} kg CO₂</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  item: {
    marginBottom: 15,
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Ajustes dinamicos backend (app.js): 

@app.route('/ajustar_dificultad', methods=['GET'])
def ajustar_dificultad():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    # Analizar el rendimiento pasado
    misiones_completadas = usuario.misiones_completadas
    dificultad_actual = usuario.dificultad_actual

    # Lógica para ajustar la dificultad
    if misiones_completadas >= 10:
        nueva_dificultad = dificultad_actual + 1  # Aumentar la dificultad
    else:
        nueva_dificultad = dificultad_actual - 1  # Reducir la dificultad

    usuario.dificultad_actual = max(1, nueva_dificultad)  # Nunca bajamos de 1
    db.session.commit()

    return jsonify({'message': 'Dificultad ajustada', 'nueva_dificultad': usuario.dificultad_actual})


- Recopilacion de datos (Backend) (app.py)

@app.route('/registrar_actividad', methods=['POST'])
def registrar_actividad():
    data = request.json
    usuario_id = data.get('usuario_id')
    tipo_actividad = data.get('tipo_actividad')
    cantidad = data.get('cantidad')
    huella_carbono = calcular_huella_carbono(tipo_actividad, cantidad)  # Función para calcular la huella
    nueva_actividad = ActividadUsuario(
        usuar


- Modelo de Recomendaciones (Backend): 

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import create_engine

def reentrenar_modelo():
    # Conectar a la base de datos
    engine = create_engine('postgresql://user:password@localhost/huella_carbono_db')
    df = pd.read_sql('SELECT * FROM actividad_usuario', engine)

    # Definir las características (features) y el objetivo (target)
    X = df[['tipo_actividad', 'cantidad', 'dia_semana']]  # Características
    y = df['huella_carbono']  # Objetivo: huella de carbono

    # Convertir variables categóricas a numéricas
    X = pd.get_dummies(X, columns=['tipo_actividad', 'dia_semana'])

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    modelo = RandomForestRegressor()
    modelo.fit(X_train, y_train)

    # Guardar el modelo entrenado para uso futuro
    with open('modelo_huella_carbono.pkl', 'wb') as file:
        pickle.dump(modelo, file)

    print("Modelo reentrenado y guardado con éxito")

# Reentrenar el modelo semanalmente
if __name__ == '__main__':
    reentrenar_modelo()



- Feedback recomendaciones (backend) (app.py): 

@app.route('/feedback_recomendacion', methods=['POST'])
def feedback_recomendacion():
    data = request.json
    usuario_id = data.get('usuario_id')
    recomendacion_id = data.get('recomendacion_id')
    feedback = data.get('feedback')  # 1 para positivo, 0 para negativo

    nueva_feedback = FeedbackRecomendacion(
        usuario_id=usuario_id,
        recomendacion_id=recomendacion_id,
        feedback=feedback
    )
    db.session.add(nueva_feedback)
    db.session.commit()

    return jsonify({'message': 'Gracias por tu feedback'})


- Comportamineto Futuro (Backend) (app.py): 

@app.route('/prediccion_comportamiento', methods=['GET'])
def prediccion_comportamiento():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    # Extraer datos históricos
    actividades = ActividadUsuario.query.filter_by(usuario_id=usuario_id).all()

    # Simular comportamiento futuro basado en patrones actuales
    huella_futura = simular_huella_futura(actividades)  # Función que predice el impacto futuro

    return jsonify({'huella_futura': huella_futura})


- Simulacion comportamiento: 

def simular_huella_futura(actividades):
    # Análisis simple para estimar la huella de carbono futura
    media_actividad = sum([a.huella_carbono for a in actividades]) / len(actividades)

    # Predicción para los próximos 30 días
    huella_futura = media_actividad * 30

    return huella_futura


- IMpacto futuro (Frontend) (ImpactoFuturo.js)

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import axios from 'axios';
import { LineChart } from 'react-native-chart-kit';

export default function ImpactoFuturo() {
  const [huellaFutura, setHuellaFutura] = useState([]);

  useEffect(() => {
    const obtenerImpactoFuturo = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/prediccion_comportamiento', {
          params: { usuario_id: 1 }
        });
        setHuellaFutura(response.data.huella_futura);
      } catch (error) {
        console.error('Error al obtener la predicción futura', error);
      }
    };

    obtenerImpactoFuturo();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Impacto de tu Comportamiento Futuro</Text>
      <LineChart
        data={{
          labels: ["Día 1", "Día 10", "Día 20", "Día 30"],
          datasets: [{ data: huellaFutura }]
        }}
        width={320}
        height={220}
        yAxisLabel="kg "
        chartConfig={{
          backgroundColor: "#e26a00",
          backgroundGradientFrom: "#fb8c00",
          backgroundGradientTo: "#ffa726",
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
        style={{ marginVertical: 8, borderRadius: 16 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
});


- Implementar Aprendizaje por Refuerzo (Backend): 

import numpy as np

# Inicializamos la tabla Q
q_table = np.zeros([estado_n, accion_n])

# Parámetros de aprendizaje
alpha = 0.1
gamma = 0.6
epsilon = 0.1

def ajustar_dificultad_q_learning(estado, accion, recompensa, nuevo_estado):
    predecir = q_table[estado, accion]
    # Actualizamos la tabla Q
    q_table[estado, accion] = predecir + alpha * (recompensa + gamma * np.max(q_table[nuevo_estado]) - predecir)


- Dificultad Dinámica en el Frontend ( Misiones.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

export default function Misiones() {
  const [misiones, setMisiones] = useState([]);
  const [dificultad, setDificultad] = useState(1);

  useEffect(() => {
    const obtenerMisiones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/obtener_misiones', {
          params: { usuario_id: 1 }
        });
        setMisiones(response.data.misiones);
        setDificultad(response.data.dificultad_actual);
      } catch (error) {
        console.error('Error al obtener las misiones', error);
      }
    };

    obtenerMisiones();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tus Misiones (Dificultad: {dificultad})</Text>
      {misiones.map((mision, index) => (
        <View key={index} style={styles.mision}>
          <Text>{mision.descripcion}</Text>
          <Button title="Completar Misión" onPress={() => Alert.alert('Misión Completada')} />
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  mision: {
    marginBottom: 15,
    padding: 15,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- Factores Contextuales (Backend) (app.py): 


@app.route('/generar_recomendaciones', methods=['GET'])
def generar_recomendaciones():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    # Obtener datos contextuales
    ubicacion = obtener_ubicacion_actual(usuario_id)  # Función que obtendría la ubicación del usuario
    clima = obtener_datos_climaticos(ubicacion)  # Función para obtener datos climáticos

    # Generar recomendaciones con IA
    recomendaciones = generar_recomendaciones_ia(usuario, ubicacion, clima)
    
    return jsonify({'recomendaciones': recomendaciones})


- Datos IoT (Backend) (app.py): 

@app.route('/integrar_iot', methods=['POST'])
def integrar_iot():
    data = request.json
    usuario_id = data.get('usuario_id')
    dispositivo_id = data.get('dispositivo_id')
    consumo_energia = data.get('consumo_energia')

    # Guardar datos del dispositivo IoT
    nueva_entrada = DispositivoIot(
        usuario_id=usuario_id,
        dispositivo_id=dispositivo_id,
        consumo_energia=consumo_energia
    )
    db.session.add(nueva_entrada)
    db.session.commit()

    return jsonify({'message': 'Datos IoT registrados'})


- Implementar Clustering con K-Means (Backend) (models.py): 

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    puntos = db.Column(db.Integer, default=0)
    cluster_id = db.Column(db.Integer)  # Identificador del clúster al que pertenece el usuario


- Algoritmo Cluster (Backend): 

from sklearn.cluster import KMeans
import pandas as pd
from sqlalchemy import create_engine

def realizar_clustering():
    # Conectar a la base de datos
    engine = create_engine('postgresql://user:password@localhost/huella_carbono_db')
    df = pd.read_sql('SELECT * FROM actividad_usuario', engine)

    # Seleccionar las características para el clustering (actividades, huella de carbono, etc.)
    X = df[['cantidad', 'huella_carbono']]

    # Aplicar K-Means para encontrar grupos
    kmeans = KMeans(n_clusters=5)  # Dividimos a los usuarios en 5 grupos
    df['cluster'] = kmeans.fit_predict(X)

    # Guardar los resultados de clustering en la base de datos
    for index, row in df.iterrows():
        usuario = Usuario.query.get(row['usuario_id'])
        usuario.cluster_id = row['cluster']
        db.session.commit()

    print("Clustering realizado con éxito")

if __name__ == '__main__':
    realizar_clustering()

- Generar recomendaciones por clúster (Backend) (app.py): 

@app.route('/recomendaciones_cluster', methods=['GET'])
def recomendaciones_cluster():
    usuario_id = request.args.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    # Obtener el clúster del usuario
    cluster_id = usuario.cluster_id

    # Generar recomendaciones para el clúster
    recomendaciones = obtener_recomendaciones_por_cluster(cluster_id)
    
    return jsonify({'recomendaciones': recomendaciones})

- Anomalias Backned: 

from sklearn.ensemble import IsolationForest

def detectar_anomalias():
    # Conectar a la base de datos
    engine = create_engine('postgresql://user:password@localhost/huella_carbono_db')
    df = pd.read_sql('SELECT * FROM actividad_usuario', engine)

    # Seleccionar las características relevantes (cantidad, huella de carbono)
    X = df[['cantidad', 'huella_carbono']]

    # Aplicar Isolation Forest
    isolation_forest = IsolationForest(contamination=0.1)
    df['anomalia'] = isolation_forest.fit_predict(X)

    # Marcar las anomalías en la base de datos
    for index, row in df.iterrows():
        if row['anomalia'] == -1:  # Si es una anomalía
            actividad = ActividadUsuario.query.get(row['id'])
            actividad.es_anomalia = True
            db.session.commit()

    print("Detección de anomalías completada")

- Alerta sobre anomalias (Backend): 

@app.route('/alerta_anomalia', methods=['GET'])
def alerta_anomalia():
    usuario_id = request.args.get('usuario_id')
    actividades = ActividadUsuario.query.filter_by(usuario_id=usuario_id, es_anomalia=True).all()

    if actividades:
        return jsonify({'message': 'Se ha detectado un comportamiento anómalo en tu actividad'})
    else:
        return jsonify({'message': 'Todo normal con tus hábitos'})


- Alerta anomalias forntend (AlertasAnomalas.js):

import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

export default function AlertasAnomalas() {
  const [alertas, setAlertas] = useState([]);

  useEffect(() => {
    const obtenerAlertas = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/alerta_anomalia', {
          params: { usuario_id: 1 }
        });
        setAlertas(response.data.alertas);
      } catch (error) {
        console.error('Error al obtener las alertas', error);
      }
    };

    obtenerAlertas();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Alertas de Comportamiento Anómalo</Text>
      <FlatList
        data={alertas}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.alerta}>
            <Text>{item.descripcion}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  alerta: {
    padding: 10,
    marginBottom: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});


- chatbot (Backend) (app.py): 

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    usuario_id = data.get('usuario_id')
    mensaje = data.get('mensaje').lower()

    # Respuesta personalizada basada en el mensaje del usuario
    if "progreso" in mensaje:
        return mostrar_progreso_usuario(usuario_id)
    elif "recomendacion" in mensaje or "sugerencia" in mensaje:
        return generar_recomendacion(usuario_id)
    elif "impacto futuro" in mensaje:
        return predecir_impacto_futuro(usuario_id)
    else:
        return jsonify({'respuesta': 'Lo siento, no entiendo tu mensaje. ¿Puedes reformularlo?'})


- Chatbot (Frontend) (Chatbot.js): 

import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

export default function Chatbot() {
  const [mensajes, setMensajes] = useState([]);
  const [mensajeActual, setMensajeActual] = useState('');

  const enviarMensaje = async () => {
    const nuevoMensaje = { tipo: 'usuario', texto: mensajeActual };
    setMensajes([...mensajes, nuevoMensaje]);

    try {
      const response = await axios.post('http://127.0.0.1:5000/chatbot', {
        usuario_id: 1,
        mensaje: mensajeActual,
      });
      setMensajes([...mensajes, nuevoMensaje, { tipo: 'bot', texto: response.data.respuesta }]);
    } catch (error) {
      console.error('Error al enviar el mensaje al chatbot', error);
    }

    setMensajeActual('');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Habla con CarbonTrackAI</Text>
      <FlatList
        data={mensajes}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={item.tipo === 'usuario' ? styles.mensajeUsuario : styles.mensajeBot}>
            <Text>{item.texto}</Text>
          </View>
        )}
      />
      <TextInput
        value={mensajeActual}
        onChangeText={setMensajeActual}
        placeholder="Escribe tu mensaje..."
        style={styles.input}
      />
      <Button title="Enviar" onPress={enviarMensaje} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  mensajeUsuario: {
    alignSelf: 'flex-end',
    backgroundColor: '#daf5d0',
    padding: 10,
    borderRadius: 5,
    marginBottom: 10,
  },
  mensajeBot: {
    alignSelf: 'flex-start',
    backgroundColor: '#f0f0f0',
    padding: 10,
    borderRadius: 5,
    marginBottom: 10,
  },
  input: {
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
});



-Chatbot Backend Nlp : 

import spacy

nlp = spacy.load('en_core_web_sm')

def interpretar_mensaje(mensaje):
    doc = nlp(mensaje)
    if any(token.lemma_ == "progreso" for token in doc):
        return "progreso"
    elif any(token.lemma_ == "recomendación" for token in doc):
        return "recomendacion"
    else:
        return "desconocido"


- Nuevo Clustering (Backeend): 


from sklearn.cluster import DBSCAN

def realizar_clustering_avanzado():
    engine = create_engine('postgresql://user:password@localhost/huella_carbono_db')
    df = pd.read_sql('SELECT * FROM actividad_usuario', engine)

    X = df[['cantidad', 'huella_carbono']]

    # Aplicar DBSCAN
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    df['cluster'] = dbscan.fit_predict(X)

    for index, row in df.iterrows():
        usuario = Usuario.query.get(row['usuario_id'])
        usuario.cluster_id = row['cluster']
        db.session.commit()


Ofrecer Recomendaciones Grupales Basadas en Clustering (Backend): 

def obtener_recomendaciones_por_cluster(cluster_id):
    recomendaciones_grupo = Recomendacion.query.filter_by(cluster_id=cluster_id).all()
    return [{'descripcion': r.descripcion} for r in recomendaciones_grupo]


Progreso Frontend: 

import React from 'react';
import { View, Text } from 'react-native';
import { BarChart } from 'react-native-chart-kit';

export default function ProgresoComparativo({ progresoUsuario, progresoGrupo }) {
  return (
    <View>
      <Text>Tu Progreso vs. Grupo</Text>
      <BarChart
        data={{
          labels: ['Tú', 'Grupo'],
          datasets: [{ data: [progresoUsuario, progresoGrupo] }]
        }}
        width={320}
        height={220}
        yAxisLabel="kg "
        chartConfig={{
          backgroundColor: '#e26a00',
          backgroundGradientFrom: '#fb8c00',
          backgroundGradientTo: '#ffa726',
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
      />
    </View>
  );
}


- Notificaciones anomalias y misones (Backend) (app.py): 

@app.route('/enviar_notificacion', methods=['POST'])
def enviar_notificacion():
    data = request.json
    usuario_id = data.get('usuario_id')
    tipo_notificacion = data.get('tipo')

    # Crear notificación en la base de datos
    nueva_notificacion = Notificacion(
        usuario_id=usuario_id,
        tipo=tipo_notificacion,
        mensaje="Has completado una nueva misión"
    )
    db.session.add(nueva_notificacion)
    db.session.commit()

    return jsonify({'message': 'Notificación enviada'})


Visualizacion de notificaciones (Frontend) ( Notificaciones.js): 

import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

export default function Notificaciones() {
  const [notificaciones, setNotificaciones] = useState([]);

  useEffect(() => {
    const obtenerNotificaciones = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/notificaciones', {
          params: { usuario_id: 1 }
        });
        setNotificaciones(response.data.notificaciones);
      } catch (error) {
        console.error('Error al obtener notificaciones', error);
      }
    };

    obtenerNotificaciones();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tus Notificaciones</Text>
      <FlatList
        data={notificaciones}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.notificacion}>
            <Text>{item.mensaje}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  notificacion: {
    padding: 10,
    marginBottom: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
});













