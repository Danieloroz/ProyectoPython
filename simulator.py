import requests
import random
import time

# Identificador del sensor: 'HHHH1234' -> (Ejemplo: 'JDOE5678')
SENSOR_ID = "JDOC1234"

# URL de la API Flask
API_URL = "http://127.0.0.1:5000/data"

def simulate_sensor():
    while True:
        # Generar valor aleatorio (simulando un sensor natural)
        sensor_value = round(random.uniform(10, 50), 2)  # Ej: Temperatura en grados
        data = {
            "sensor_id": SENSOR_ID,
            "value": sensor_value,
        }
        
        # Enviar datos a la API
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                print(f"Datos enviados: {data}")
            else:
                print(f"Error al enviar datos: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
        
        # Pausa antes de enviar el siguiente dato
        time.sleep(5)  # Intervalo de 5 segundos

if __name__ == "__main__":
    simulate_sensor()