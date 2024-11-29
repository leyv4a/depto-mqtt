import json
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.mqtt_client import create_mqtt_client


# Configuración inicial del HVAC
hvac_state = {
    "estado": "OFF",
    "temperatura_inicial": 22.0,  # Temperatura inicial
    "temperatura_objetivo": None
}

def on_message(client, userdata, msg):
    """Callback para manejar mensajes de comandos HVAC."""
    global hvac_state
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[HVAC CONTROL] Mensaje recibido en {topic}: {payload}", flush=True)

    # Procesar comandos HVAC
    if topic.endswith("command"):
        try:
            command = json.loads(payload)
            action = command.get("action")
            target_temperature = command.get("temperatura_objetivo")

            if action == "ON":
                hvac_state["estado"] = "ON"
                hvac_state["temperatura_objetivo"] = target_temperature
                print("[HVAC CONTROL] HVAC encendido.", flush=True)

            elif action == "OFF":
                hvac_state["estado"] = "OFF"
                hvac_state["temperatura_objetivo"] = None
                print("[HVAC CONTROL] HVAC apagado.", flush=True)

            # Publicar estado actualizado
            publish_state(client)

        except json.JSONDecodeError:
            print("[HVAC CONTROL] Error al procesar el comando: Formato JSON invalido.", flush=True)

def publish_state(client):
    """Publica el estado actual del HVAC como mensaje retenido."""
    state_topic = "control/A/hvac/status"
    state_payload = json.dumps(hvac_state)
    client.publish(state_topic, state_payload, retain=True)
    print(f"[HVAC CONTROL] Estado publicado: {state_payload}", flush=True)

if __name__ == "__main__":
    client_id = "hvac_control"
    client = create_mqtt_client(client_id)
    client.on_message = on_message

    # Suscribirse al tópico de comandos HVAC
    command_topic = "control/A/hvac/command"
    client.subscribe(command_topic)
    print(f"[HVAC CONTROL] Suscrito al topico: {command_topic}", flush=True)

    # Publicar estado inicial
    publish_state(client)

    print("[HVAC CONTROL] Escuchando comandos...", flush=True)
    client.loop_forever()