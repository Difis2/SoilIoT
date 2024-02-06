#!/usr/bin/python3

User = "my-app-2000@ttn"
Password = "NNSXS.2SRZDRU5C6UD32MDHYKSFW7TFBOEGBKWNQESKCI.3EJOGRSVJ5TSGT7QP2M7FXEW7TNIQOYU577G2QX43QYLDOTWJB5Q"
theRegion = "EU1"		# The region you are using
s=""


VER  = "2021-05-24 v1.2"
import base64
import os, sys, logging, time
print(os.path.basename(__file__) + " " + VER)

print("Imports:")
import paho.mqtt.client as mqtt
import json
import csv
from datetime import datetime
import sqlite3


mqtt_data = { 
    'temperature': 0.0,
    'humidity': 0.0,
    'soil_humidity': 0.0,
    'soil_temperature': 0.0,
    'n': 0.0,
    'p': 0.0,
    'k': 0.0,
}
count=0
lock=0

print("Functions:")
# Write uplink to tab file


# MQTT event functions
def on_connect(mqttc, obj, flags, rc):
    print("\nConnect: rc = " + str(rc))
    
def getData(someJSON):
    global mqtt_data
    uplink_message = someJSON["uplink_message"]
    decoded_payload = uplink_message["decoded_payload"]
    mqtt_data['n'] = decoded_payload["n"]
    mqtt_data['p'] = decoded_payload["p"]
    mqtt_data['k'] = decoded_payload["k"]
    print(mqtt_data)

def base64ToHexa(someJSON):
	uplink_message = someJSON["uplink_message"]
	frm_payload = uplink_message["frm_payload"]
	decoded_bytes = base64.b64decode(frm_payload)
	hexa=decoded_bytes.hex()
	return hexa
def on_message2(mqttc, obj, msg):

    if "count" not in on_message2.__dict__:
        on_message2.count = 0

    words = msg.topic.split("/")
    last_word = words[-1]

    if last_word == 'up':
        on_message2.count += 1
        print(f"Count: {on_message2.count}")
        if on_message2.count % 2 == 0:
            parsedJSON = json.loads(msg.payload)
            getData(parsedJSON)
            global lock
            lock = lock + 1;
            if (lock == 2):
                insert_mqtt_data(lock,mqtt_data['temperature'], mqtt_data['humidity'], mqtt_data['soil_humidity'], mqtt_data['soil_temperature'], mqtt_data['n'], mqtt_data['p'], mqtt_data['k'])

# Function to insert MQTT data into the database
def insert_mqtt_data(temperature, humidity, soil_humidity, soil_temperature, n , p, k):
    global lock
    lock=0
    if is_morning() and count == 0:
        count = 1 
    
        conn = sqlite3.connect('mqtt_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mqtt_data (location, temperature, humidity, soil_humidity, soil_temperature)
            VALUES (?, ?, ?, ?)
        ''', (temperature, humidity, soil_humidity,soil_temperature, n, p, k))
        conn.commit()
        conn.close()


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("\nSubscribe: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print("\nLog: "+ string)
    logging_level = mqtt.LOGGING_LEVEL[level]
    logging.log(logging_level, string)



print("Body of program:")
User = "my-app-2000@ttn"
Password = "NNSXS.2SRZDRU5C6UD32MDHYKSFW7TFBOEGBKWNQESKCI.3EJOGRSVJ5TSGT7QP2M7FXEW7TNIQOYU577G2QX43QYLDOTWJB5Q"
theRegion = "EU1"
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message2
mqttc.username_pw_set(User, Password)
mqttc.tls_set()
mqttc.connect(theRegion.lower() + ".cloud.thethings.network", 8883, 60)


print("Subscribe")
mqttc.subscribe("#", 0)	# all device uplinks

print("And run forever")
try:    
	run = True
	while run:
		mqttc.loop(10) 	# seconds timeout / blocking time

		
    
except KeyboardInterrupt:
    print("Exit")
    sys.exit(0)