import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.mqtt_client import create_mqtt_client

def on_message(client, userdata, msg):
    """Callback para procesar los mensajes recibidos."""
    print(f"[MONITOR] Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

if __name__ == "__main__":
    client_id = "monitor_client"
    client = create_mqtt_client(client_id)
    
    # Configurar el callback para procesar mensajes
    client.on_message = on_message

    # Suscribirse a los tópicos especificados
    topics = [
        ("departamentos/+/1/+/+", 0),  # Monitoreo por piso (ejemplo: piso 1)
        ("departamentos/+/+/+/temperatura", 0),  # Monitoreo por tipo de sensor
    ]
    
    for topic, qos in topics:
        client.subscribe(topic, qos)
        print(f"[MONITOR] Suscrito al tópico: {topic}")

    print("[MONITOR] Escuchando mensajes...")
    client.loop_forever()