from utils.mqtt_client import create_mqtt_client

def on_message(client, userdata, msg):
    """Callback cuando se recibe un mensaje."""
    print(f"Mensaje recibido: {msg.payload.decode()} en el tópico {msg.topic}")

if __name__ == "__main__":
    client_id = "monitor_test"
    client  = create_mqtt_client(client_id)
    
    # Cambia el tópico según lo que desees monitorear
    client.subscribe("departamentos/A/1/101/#")
    client.on_message = on_message

    print("Escuchando mensajes...")
    client.loop_forever()