import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("dragino-1ed75c/2231375/data")
    else:
        print("Connection failed with error code:", rc)

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    topic = message.topic
    print("Received message:", payload, "on topic:", topic)
    # Add your data processing logic here

# Create an MQTT client instance
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
mqtt_broker_ip = "192.168.1.69"
mqtt_broker_port = 1883
client.connect(mqtt_broker_ip, mqtt_broker_port)

# Start the MQTT loop
client.loop_start()

# Keep the script running to receive messages
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Terminating...")
finally:
    client.loop_stop()
    client.disconnect()