import json
from random import uniform, random
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

config = config["departamento1"]
ubicacion = config["ubicacion"]
sensores = config["sensores"]
intervalo = config["publicacion"]["intervalo_segundos"]

# Extraer umbrales
umbral_temp = sensores["temperatura"]["umbral_alerta"]
prob_fuga = sensores["fuga_agua"]["probabilidad_activacion"]

# Crear cliente MQTT
client_id = f"sensor-depto-{ubicacion['edificio']}"
client = create_mqtt_client(client_id)
client.loop_start()

# Generar tópicos
topic_temp = f"departamentos/{ubicacion['edificio']}/{ubicacion['piso']}/temperatura"
topic_fuga = f"departamentos/{ubicacion['edificio']}/{ubicacion['piso']}/fuga_agua"
topic_alerta = f"alerts/{ubicacion['edificio']}/{ubicacion['piso']}"

client.loop_start()
print(f"[DEPTO1] Publicando datos en {topic_temp} y {topic_fuga}", flush=True)

# Publicar datos de sensores
try:
    while True:
        temperatura = round(uniform(sensores["temperatura"]["min"], sensores["temperatura"]["max"]), 2)
        fuga_agua = "ALERTA" if random() < prob_fuga else "SIN_FUGA"
        
        # Publicar temperatura
        client.publish(topic_temp, temperatura, retain=True)
        print(f"[DEPTO1] Publicado {temperatura} en {topic_temp}", flush=True)

         # Publicar estado de fuga
        client.publish(topic_fuga, fuga_agua, retain=True)
        print(f"[DEPTO1] Publicado {fuga_agua} en {topic_fuga}", flush=True)
        

          # Verificar y publicar alertas
        if temperatura > umbral_temp:
            alerta_temp = f"ALERTA: Temperatura alta ({temperatura}°C) supera umbral ({umbral_temp}°C)"
            client.publish(topic_alerta, alerta_temp, retain=True)
            print(f"[ALERTA] Publicado {alerta_temp} en {topic_alerta}", flush=True)
        
        if fuga_agua == "ALERTA":
            alerta_fuga = "ALERTA: Fuga de agua detectada"
            client.publish(topic_alerta, alerta_fuga, retain=True)
            print(f"[ALERTA] Publicado {alerta_fuga} en {topic_alerta}", flush=True)
        
        time.sleep(intervalo)
except KeyboardInterrupt:
    print("[DEPTO1] Finalizando publicación...")
finally:
    client.loop_stop()
    client.disconnect()