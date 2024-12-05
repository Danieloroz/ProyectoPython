import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

# Inicializar la app de Firebase con las credenciales
cred = credentials.Certificate('api/sensor-de-movimiento-93214-firebase-adminsdk-hvrxp-4a05414d8a.json')
firebase_admin.initialize_app(cred)

# Inicializar Firestore
db = firestore.client()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Función para almacenar datos en Firebase
def store_data(sensor_data):
    # Referencia a la colección "sensores"
    sensor_ref = db.collection('sensores')
    
    # Crear un nuevo documento con datos
    sensor_ref.add(sensor_data)

@app.route('/')
def index():
    # Recupera todos los sensores disponibles desde Firebase (o una base de datos)
    sensors_ref = db.collection('sensores')
    sensors = [doc.id for doc in sensors_ref.stream()]  # Lista de ids de sensores
    return render_template('index.html', sensors=sensors)


# Ruta para recibir datos del sensor
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    # Validar datos recibidos
    if not data or 'sensor_id' not in data or 'value' not in data:
        return jsonify({"error": "Datos invalidos"}), 400

    # Obtener la fecha y hora actual
    timestamp = datetime.now()
    date = timestamp.date().isoformat()  # Fecha en formato YYYY-MM-DD
    time = timestamp.time().strftime('%H:%M:%S')  # Hora en formato HH:MM:SS
    
    # Estructura de datos que se guardará en Firestore
    sensor_data = {
        'date': date,
        'time': time,
        'sensor_id': data['sensor_id'],
        'value': data['value']
    }
    
    # Almacenar datos en Firebase
    store_data(sensor_data)

    return jsonify({"message": "Datos recibidos correctamente", "data": sensor_data}), 200

# Ruta para obtener los datos almacenados
@app.route('/data', methods=['GET'])
def get_data():
    # Obtener los datos de Firestore
    sensor_ref = db.collection('sensores')
    docs = sensor_ref.stream()

# Convertir los documentos a una lista de diccionarios
    all_data = []
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id  # Añadir el ID del documento de Firestore
        all_data.append(doc_dict)

    return jsonify(all_data), 200

if __name__ == '__main__':
    app.run(debug=True)


