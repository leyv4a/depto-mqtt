import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.mqtt_client import create_mqtt_client

config_dir = os.path.join(os.path.dirname(__file__), "../config")
# Leer configuración de umbrales desde settings.json
with open(os.path.join(config_dir, "settings.json")) as config_file:
    config = json.load(config_file)

temperature_threshold = config["thresholds"]["temperatura"]
water_leakage_alert = config["thresholds"]["fuga_activa"]

def on_message(client, userdata, msg):
    """Callback para procesar los mensajes recibidos."""
    payload = msg.payload.decode()
    print(f"[MONITOR] Mensaje recibido en {msg.topic}: {payload}")
    
    # Procesar el mensaje según el tópico
    topic_parts = msg.topic.split("/")
    if len(topic_parts) >= 5 and topic_parts[4] == "temperatura":
        try:
            temperature = float(payload)
            if temperature > temperature_threshold:
                alert_topic = f"alerts/{topic_parts[1]}/temperatura"
                alert_message = f"ALERTA: Temperatura crítica detectada: {temperature}°C"
                client.publish(alert_topic, alert_message, retain=True)
                print(f"[ALERTA] {alert_message}")
        except ValueError:
            print("[ERROR] Valor de temperatura inválido.")
    elif len(topic_parts) >= 5 and topic_parts[4] == "fuga_agua":
        if payload.lower() == "true":
            alert_topic = f"alerts/{topic_parts[1]}/fuga_agua"
            alert_message = "ALERTA: Detección de fuga de agua."
            client.publish(alert_topic, alert_message, retain=True)
            print(f"[ALERTA] {alert_message}")

if __name__ == "__main__":
    client_id = "monitor_client"
    client = create_mqtt_client(client_id)
    
    # Configurar el callback para procesar mensajes
    client.on_message = on_message

    # Suscribirse a los tópicos relevantes
    topics = [
        ("departamentos/+/1/+/+", 0),  # Monitoreo por piso (ejemplo: piso 1)
        ("departamentos/+/+/+/temperatura", 0),  # Monitoreo por tipo de sensor
        ("departamentos/+/+/+/fuga_agua", 0),  # Monitoreo de fugas de agua
    ]
    
    for topic, qos in topics:
        client.subscribe(topic, qos)
        print(f"[MONITOR] Suscrito al tópico: {topic}")

    print("[MONITOR] Escuchando mensajes...")
    client.loop_forever()