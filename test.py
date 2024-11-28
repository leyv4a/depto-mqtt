from utils.mqtt_client import create_mqtt_client

def main():
    client = create_mqtt_client("test-client")  # Identificador único para este cliente
    client.loop_start()  # Inicia el loop para manejar la comunicación MQTT
    
    # Prueba de publicación
    topic = "test/topic"
    message = "Hello, MQTT!"
    client.publish(topic, message)
    print(f"Publicado: {message} en el tópico: {topic}")
    
    # Esperar un poco para recibir mensajes (si los hay)
    import time
    time.sleep(5)

    client.loop_stop()  # Detiene el loop
    client.disconnect()  # Desconecta del broker


if __name__ == "__main__":
    main()
