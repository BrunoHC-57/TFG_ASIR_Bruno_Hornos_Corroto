import random
import time
import json
import paho.mqtt.client as mqtt

#Colores para las letras
from colorama import Fore, Style, init

init(autoreset=True)

#Datos
nombre = "Cinta_1"
estado = "Funcionando"
temperaturas = 60.0
velocidad = 1.5
horas = 124.0
produccion = 0
averia = False

#Recepcion de comandos por mqtt
def recibir_comando(cliente, userdata, msg):
    comando = msg.payload.decode()

    print(f"Comando recibido: {comando}")


#creacion de cliente
cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_message = recibir_comando
cliente.connect("localhost", 1883, 60)
cliente.subscribe("smartfactory/cinta1/comandos")
cliente.loop_start()

#Inicio

print(f"iniciando simulacion de: ", nombre)
print("-----------------------------------------")

#bucle para que varien automaticamente los parametros de funcionamiento de la maquina para simular un funcionamiento real que pueda dar fallos.
while True:
    #Control de averia
    if not averia:
        temperaturas += random.uniform(-1, 2)  

        #Control de temperatura
        if temperaturas > 80:
            estado = "ERROR"
            velocidad = 0
            #Aviso de averia
            averia = True
            
            # msg de alerta de fallo
            print()
            print(Fore.RED + "======================================================")
            print(Fore.YELLOW + f"⚠ AVERIA DETECTADA EN {nombre}")
            print("Motivo: SOBRECALENTAMIENTO")
            print(f"Temperatura: {temperaturas:.1f} ºC")
            print("Maquina detenida por seguridad")
            print("Esperando intervencion del tecnico...")
            print(Fore.RED + "======================================================")
        elif temperaturas > 70:
            estado = "WARNING"
        else:
            estado = "Funcionando"

        #Parada de emergencia si hay error si no funciona con normalidad.
        if estado == "ERROR":
            velocidad = 0
        else:
            velocidad += random.uniform(-0.05, 0.05)
            horas += 0.1
            produccion += random.randint(1, 5)

        #Cambio de color segun el estado de la maquina
        if estado == "Funcionando":
            color_estado = Fore.GREEN
        elif estado == "WARNING":
            color_estado = Fore.YELLOW
        else:
            color_estado = Fore.RED

        #Guardado de datos 
        datos = {
            "Nombre": nombre,
            "Estado": estado,
            "Temperatura": round(temperaturas, 1),
            "Velocidad": round(velocidad, 2),
            "Horas": round(horas, 1),
            "Produccion": produccion
        }

        #Se pasa a json
        mensaje_json = json.dumps(datos)

        #Se publica el json
        cliente.publish(
            "smartfactory/cinta1/telemetria",
            mensaje_json
        )

        print(
            f"{nombre} | "
            f"{color_estado}{estado}{Style.RESET_ALL} | "
            f"Temperatura: {temperaturas:.1f} ºC | "
            f"Velocidad: {velocidad:.2f} m/s | "
            f"Horas: {horas:.1f} | "
            f"Produccion: {produccion} | "
        )

    time.sleep(2)