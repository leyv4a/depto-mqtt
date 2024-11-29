import sys
import os
import json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.mqtt_client import create_mqtt_client

config_dir = os.path.join(os.path.dirname(__file__), "../config")
# Leer configuración de umbrales desde settings.json
with open(os.path.join(config_dir, "settings.json")) as config_file:
    config = json.load(config_file)

thresholds = config["thresholds"]

def send_hvac_command(client, action, temperatura_objetivo):
    """Envia un comando al HVAC."""
    print(f"ENVIANDO COMANDO SEND_HVAC")
    command_topic = "control/A/hvac/command"
    command_payload = {
        "action": action,
        "temperatura_objetivo": temperatura_objetivo
    }
    client.publish(command_topic, json.dumps(command_payload))
    print(f"[MONITOR] Comando enviado al HVAC: {command_payload}", flush=True)

# Función para manejar mensajes

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    # print(f"[MONITOR] Mensaje recibido en {topic}: {payload}", flush=True)
    
    if topic.startswith("alerts/"):
        if "ALERTA: Temperatura alta" in payload:
            print("[MONITOR] Temperatura alta detectada. Enviando comando al HVAC...", flush=True)
            send_hvac_command(client, action="ON", temperatura_objetivo=25.0)
        else:
            print(f"[ALERTA] Mensaje critico recibido: {payload} en {topic}", flush=True)

    elif topic.startswith("control/A/hvac/status"):
        print(f"[MONITOR] Estado del HVAC actualizado: {payload}", flush=True)

    elif topic.startswith("control/"):
        print(f"[CONTROL] Comando recibido: {payload} en {topic}", flush=True)

# Publicar configuración del sistema
def publish_config(client):
    config_topic = "system/config"
    config_payload = json.dumps(thresholds)
    client.publish(config_topic, config_payload, retain=True)
    print(f"[CONFIG] Configuracion publicada en {config_topic}: {config_payload}", flush=True)

# Configuración del cliente
if __name__ == "__main__":
    client_id = "monitor_client"
    client = create_mqtt_client(client_id)
    client.on_message = on_message

    # Publicar config del sistema
    publish_config(client)

    # Suscribirse a los topicos con wildcards
    topics = [
        # ("departamentos/+/+/temperatura", 0),  # Monitoreo por tipo de sensor (temperatura)
        ("alerts/+/+", 0),                  # Monitoreo de alertas generales
        ("control/+/hvac/#", 0),            # Monitoreo del sistema de control (HVAC)
        ("control/A/hvac/status", 0)  # Estado del HVAC
    ]
    for topic, qos in topics:
        client.subscribe(topic, qos)
        print(f"[MONITOR] Suscrito al topico: {topic}", flush=True)

    print("[MONITOR] Escuchando mensajes...", flush=True)
    client.loop_forever()