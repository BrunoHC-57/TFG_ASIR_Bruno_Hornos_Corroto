import random
import time

nombre = "Cinta_1"
estado = "Funcionando"
temperaturas = 60.0
velocidad = 1.5
horas = 124.0
produccion = 0

print(f"iniciando simulacion de: ", nombre)
print("-----------------------------------------")

while True:
    temperaturas += random.uniform(-1, 1)
    velocidad += random.uniform(-0.05, 0.05)
    horas += 0.1
    produccion += random.randint(1, 5)
    print(
        f"{nombre} | "
        f"{estado} | "
        f"Temperatura: {temperaturas:.1f} ºC | "
        f"Velocidad: {velocidad:.2f} | "
        f"Horas: {horas:.1f} | "
        f"Produccion: {produccion} | "
    )

    time.sleep(2)