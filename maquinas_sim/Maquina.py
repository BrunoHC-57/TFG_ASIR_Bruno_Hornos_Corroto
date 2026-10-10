import random
import time
import json
import paho.mqtt.client as mqtt

#Colores para las letras
from colorama import Fore, Style, init

init(autoreset=True)

#Datos
class Maquina:          #Clase que representa la maquina

    def __init__(self,nombre):
        self.nombre = nombre
        self.identificador = identificador
        self.estado = "Funcionando"
        self.temperaturas = 60.0
        self.velocidad = 1.5
        self.horas = 124.0
        self.produccion = 0
        self.averia = False

    def temp_comp(self):
        if self.temperaturas > 80:
            self.estado = "ERROR"
            self.velocidad = 0
            #Aviso de averia
            self.averia = True       
            # msg de alerta de fallo
            #print()
            #print(Fore.RED + "======================================================")
            #print(Fore.YELLOW + f"⚠ AVERIA DETECTADA EN {cinta1.nombre}")
            #print("Motivo: SOBRECALENTAMIENTO")
            #print(f"Temperatura: {cinta1.temperaturas:.1f} ºC")
            #print("Maquina detenida por seguridad")
            #print("Esperando intervencion del tecnico...")
            #print(Fore.RED + "======================================================")
        elif self.temperaturas > 70:
            self.estado = "WARNING"
        else:
            self.estado = "Funcionando"

    def parada_emergencia(self):
        
        #Parada de emergencia si hay error si no funciona con normalidad.
        if self.estado == "ERROR":
            self.velocidad = 0
        else:
            self.velocidad += random.uniform(-0.05, 0.05)
            self.horas += 0.1
            self.produccion += random.randint(1, 5)

    def reseteo(self):      #docker exec -it smartfactory-mqtt mosquitto_pub -h localhost -t "smartfactory/cinta1/comandos" -m "RESET"
        if self.averia:
            self.averia = False
            self.estado = "Funcionando"
            self.temperaturas = 60
            self.velocidad = 1.5
        
            print("----------------------------------")
            print(Fore.GREEN + "Maquina reiniciada correctamente")
            print("----------------------------------")




#Maquinas:
cinta1 = Maquina("Cinta_1, cinta1")

#Recepcion de comandos por mqtt
def recibir_comando(cliente, userdata, msg):
    #decodificacion de que comando entra 
    comando = msg.payload.decode()
    print(f"Comando recibido: {comando}")

    if comando == "RESET":    #docker exec -it smartfactory-mqtt mosquitto_pub -h localhost -t "smartfactory/cinta1/comandos" -m "RESET"
        cinta1.reseteo()

#creacion de cliente
cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_message = recibir_comando
cliente.connect("localhost", 1883, 60)
cliente.subscribe("smartfactory/{cinta1.identificador}/comandos")
cliente.loop_start()

#Inicio

print(Fore.GREEN + "-----------------------------------------")
print(Fore.GREEN + f"iniciando simulacion de: ", cinta1.nombre)
print(Fore.GREEN + "-----------------------------------------")

#bucle para que varien automaticamente los parametros de funcionamiento de la maquina para simular un funcionamiento real que pueda dar fallos.
while True:
    #Control de averia
    if not cinta1.averia:
        cinta1.temperaturas += random.uniform(-1, 2)  

        cinta1.temp_comp()

        cinta1.parada_emergencia()

        #Cambio de color segun el estado de la maquina

        if cinta1.estado == "Funcionando":
            color_estado = Fore.GREEN
        elif cinta1.estado == "WARNING":
            color_estado = Fore.YELLOW
        else:
            color_estado = Fore.RED

        #Guardado de datos 
        datos = {
            "Nombre": cinta1.nombre,
            "Estado": cinta1.estado,
            "Temperatura": round(cinta1.temperaturas, 1),
            "Velocidad": round(cinta1.velocidad, 2),
            "Horas": round(cinta1.horas, 1),
            "Produccion": cinta1.produccion
        }

        #Se pasa a json
        mensaje_json = json.dumps(datos)

        #Se publica el json
        cliente.publish(
            "smartfactory/{cinta1.identificador}/telemetria",
            mensaje_json
        )

        print(
            f"{cinta1.nombre} | "
            f"{color_estado}{cinta1.estado}{Style.RESET_ALL} | "
            f"Temperatura: {cinta1.temperaturas:.1f} ºC | "
            f"Velocidad: {cinta1.velocidad:.2f} m/s | "
            f"Horas: {cinta1.horas:.1f} | "
            f"Produccion: {cinta1.produccion} | "
        )

    time.sleep(2)