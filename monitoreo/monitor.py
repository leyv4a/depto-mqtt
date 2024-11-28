import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.mqtt_client import create_mqtt_client

config_dir = os.path.join(os.path.dirname(__file__), "../config")
# Leer configuración de umbrales desde settings.json
with open(os.path.join(config_dir, "settings.json")) as config_file:
    config = json.load(config_file)

thresholds = config["thresholds"]

# Función para manejar mensajes
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MONITOR] Mensaje recibido en {topic}: {payload}")
    
    # Procesar alertas críticas
    if "temperatura" in topic:
        temperatura = float(payload)
        if temperatura > thresholds["temperatura"]:
            alert_topic = f"alerts/{topic.split('/')[1]}/temperature"
            alert_message = f"ALERTA: Temperatura crítica detectada: {temperatura}°C"
            client.publish(alert_topic, alert_message, retain=True)
            print(f"[MONITOR] Publicado {alert_message} en {alert_topic}")

# Publicar configuración del sistema
def publish_config(client):
    config_topic = "system/config"
    config_payload = json.dumps(thresholds)
    client.publish(config_topic, config_payload, retain=True)
    print(f"[CONFIG] Configuración publicada en {config_topic}: {config_payload}")

# Configuración del cliente
if __name__ == "__main__":
    client_id = "monitor_client"
    client = create_mqtt_client(client_id)
    client.on_message = on_message

    # Publicar configuración del sistema
    publish_config(client)

    # Suscribirse a los tópicos
    topics = [
        ("departamentos/+/+/+/temperatura", 0),
        ("departamentos/+/+/+/fuga_agua", 0),
    ]
    for topic, qos in topics:
        client.subscribe(topic, qos)
        print(f"[MONITOR] Suscrito al tópico: {topic}")

    print("[MONITOR] Escuchando mensajes...")
    client.loop_forever()