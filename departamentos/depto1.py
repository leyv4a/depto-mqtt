import json
import random
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.mqtt_client import create_mqtt_client

config_dir = os.path.join(os.path.dirname(__file__), "../config")
# Jalar configuraciones
with open(os.path.join(config_dir, "settings.json")) as config_file:
# with open("../config/settings.json") as config_file:
    config = json.load(config_file)

# Setear configuracion
depto_config = config["departamento1"]
ubicacion = depto_config["ubicacion"]
sensores_config = depto_config["sensores"]
intervalo = depto_config["publicacion"]["intervalo_segundos"]

# Obtener datos de ubicación
edificio = ubicacion["edificio"]
piso = ubicacion["piso"]
habitacion = ubicacion["habitacion"]

# Crear cliente MQTT
client_id = f"depto1-{edificio}-{piso}-{habitacion}"
client = create_mqtt_client(client_id)

# Publicación de datos simulados
def publicar_datos():
    while True:
        # Simular temperatura
        temperatura = round(
            random.uniform(
                sensores_config["temperature"]["min"], 
                sensores_config["temperature"]["max"]
            ), 2
        )
        topico_temperatura = f"departamentos/{edificio}/{piso}/{habitacion}/temperatura"
        client.publish(topico_temperatura, temperatura, retain=True)
        print(f"Publicado: {temperatura} en {topico_temperatura}")

        # Simular fuga de agua
        if random.random() < sensores_config["fuga_agua"]["probabilidad_activacion"]:
            fuga_estado = "ALERTA"
        else:
            fuga_estado = "SIN_FUGA"
        topico_fuga = f"departamentos/{edificio}/{piso}/{habitacion}/fuga_agua"
        client.publish(topico_fuga, fuga_estado, retain=True)
        print(f"Publicado: {fuga_estado} en {topico_fuga}")

        # Esperar antes de la próxima publicación
        time.sleep(intervalo)

if __name__ == "__main__":
    try:
        client.loop_start()
        publicar_datos()
    except KeyboardInterrupt:
        client.loop_stop()
        print("\nSimulación finalizada.")
