import random
import time
from colorama import Fore, Style, init

init(autoreset=True)

nombre = "Cinta_1"
estado = "Funcionando"
temperaturas = 60.0
velocidad = 1.5
horas = 124.0
produccion = 0

print(f"iniciando simulacion de: ", nombre)
print("-----------------------------------------")

#bucle para que varien automaticamente los parametros de funcionamiento de la maquina para simular un funcionamiento real que pueda dar fallos.
while True:
    temperaturas += random.uniform(-1, 1)
    if temperaturas > 80:
        estado = "ERROR"
        velocidad = 0
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

    print(
        f"{nombre} | "
        f"{color_estado}{estado}{Style.RESET_ALL} | "
        f"Temperatura: {temperaturas:.1f} ºC | "
        f"Velocidad: {velocidad:.2f} m/s | "
        f"Horas: {horas:.1f} | "
        f"Produccion: {produccion} | "
    )

    time.sleep(2)