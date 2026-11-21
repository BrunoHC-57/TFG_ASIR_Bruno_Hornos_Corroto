import json
import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point

# Cargar configuracion del archivo .env
load_dotenv()

# Datos de conexion con InfluxDB
url = os.getenv("INFLUXDB_URL")
token = os.getenv("INFLUXDB_TOKEN")
organizacion = os.getenv("INFLUXDB_ORG")
bucket = os.getenv("INFLUXDB_BUCKET")

# Comprobar que tenemos la configuracion
if not all([url, token, organizacion, bucket]):
    raise ValueError("Faltan datos de configuracion en .env")

# Conectar con InfluxDB
influx = InfluxDBClient(
    url=url,
    token=token,
    org=organizacion
)

escritura = influx.write_api()

# Funcion que recibe los datos MQTT
def recibir_telemetria(cliente, userdata, msg):

    try:
        datos = json.loads(msg.payload.decode())

        # Crear medicion para InfluxDB
        punto = (
            Point("maquinas")
            .tag("nombre", datos["Nombre"])
            .tag("estado", datos["Estado"])
            .field("temperatura", float(datos["Temperatura"]))
            .field("velocidad", float(datos["Velocidad"]))
            .field("horas", float(datos["Horas"]))
            .field("produccion", int(datos["Produccion"]))
        )

        # Guardar medicion
        escritura.write(
            bucket=bucket,
            org=organizacion,
            record=punto
        )

        print(f"Datos guardados: {datos['Nombre']} - {datos['Estado']}")

    except Exception as error:
        print(f"Error procesando telemetria: {error}")


# Crear cliente MQTT
cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_message = recibir_telemetria

cliente.connect("localhost", 1883, 60)
cliente.subscribe("smartfactory/+/telemetria")

print("Receptor MQTT iniciado. Esperando datos...")

# Mantener el receptor escuchando
try:
    cliente.loop_forever()
except KeyboardInterrupt:
    print("Receptor detenido")
finally:
    escritura.close()
    influx.close()