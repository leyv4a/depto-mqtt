import paho.mqtt.client as mqtt

# Configuración del broker MQTT
BROKER = "test.mosquitto.org"  # Cambia por la IP del broker si está en otra máquina
PORT = 1883
KEEPALIVE = 60

def on_connect(client, userdata, flags, rc):
    """Callback cuando se establece conexión con el broker."""
    if rc == 0:
        print("Conectado al broker MQTT")
    else:
        print(f"Error de conexión. Código: {rc}")

def on_disconnect(client, userdata, rc):
    """Callback cuando se pierde la conexión con el broker."""
    print("Desconectado del broker MQTT")

def on_message(client, userdata, msg):
    """Callback cuando se recibe un mensaje."""
    print(f"Mensaje recibido: {msg.payload.decode()} en el tópico {msg.topic}")

def create_mqtt_client(client_id):
    """
    Crea y devuelve un cliente MQTT configurado.
    
    Args:
        client_id (str): Identificador único para el cliente MQTT.
    
    Returns:
        mqtt.Client: Instancia configurada del cliente MQTT.
    """
     #cliente
    client = mqtt.Client(client_id)
    
    #callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    #  broker 
    client.connect(BROKER, PORT, KEEPALIVE)
    
    return client