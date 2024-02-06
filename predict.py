from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import joblib
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime, time
import json
#apikey ttn = NNSXS.YO7KBNS5TGJDXTKW3TDBV6F7TSH66BPBNSFXUBQ.JOVSI6UXBHFVHVSHMQI5247MUKO3U2WKVF7ANHSFIHWFGBEAJSJA
app = Flask(__name__)
CORS(app)

model = joblib.load("RandomForest.pkl")


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



def is_morning():
    now = datetime.now()
    if (now.time() < time(10, 0) and now.time() < time(9, 0)):
        return True
    else:
        return False
    
def on_connect2(mqttc, obj, flags, rc):
    print("\nConnect: rc = " + str(rc))

def on_connect1(client, userdata, flags, rc):
    if rc == 0:
        mqttClient.subscribe("dragino-1ed75c/2202439/data")
    else:
        print("Connection failed with error code:", rc)

def on_message1(client, userdata, message):
    payload = message.payload.decode('utf-8')
    topic = message.topic
    print("Received message:", payload, "on topic:", topic)

    data_components = payload.split('&')
    data = {}
    for component in data_components:
        key, value = component.split('=')
        data[key] = value
    global mqtt_data
    global count
    global lock
    mqtt_data['temperature'] = float(data.get('temp', 0.0))
    mqtt_data['humidity'] = float(data.get('hum', 0.0))
    mqtt_data['soil_humidity'] = float(data.get('soilhum', 0.0))
    mqtt_data['soil_temperature'] = float(data.get('soiltemp', 0.0))
    lock = lock + 1
    if (lock == 2):
        insert_mqtt_data(mqtt_data['temperature'], mqtt_data['humidity'], mqtt_data['soil_humidity'], mqtt_data['soil_temperature'], mqtt_data['n'], mqtt_data['p'], mqtt_data['k'])


def insert_mqtt_data(temperature, humidity, soil_humidity, soil_temperature, n , p, k):
    print("hello")
    global lock
    global count
    lock=0
    if is_morning() ==False :
        count = 1 
    
        conn = sqlite3.connect('mqtt_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mqtt_data (temperature, humidity, soil_humidity, soil_temperature, n, p, k)
            VALUES (?, ?, ?, ?, ? ,?, ?)
        ''', (temperature, humidity, soil_humidity,soil_temperature, n, p, k))
        conn.commit()
        conn.close()

def getData(someJSON):
    global mqtt_data
    uplink_message = someJSON["uplink_message"]
    decoded_payload = uplink_message["decoded_payload"]
    mqtt_data['n'] = decoded_payload["n"]
    mqtt_data['p'] = decoded_payload["p"]
    mqtt_data['k'] = decoded_payload["k"]
    print(mqtt_data)
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
            lock = lock + 1
            if (lock == 2):
                insert_mqtt_data(mqtt_data['temperature'], mqtt_data['humidity'], mqtt_data['soil_humidity'], mqtt_data['soil_temperature'], mqtt_data['n'], mqtt_data['p'], mqtt_data['k'])

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    humidity = float(data['humidity'])
    n = float(data['n'])
    p = float(data['p'])
    k = float(data['k'])
    temperature = float(data['temperature'])

    prediction = model.predict([[humidity] + [n] + [p] + [k] + [temperature]])[0]

    return jsonify({'prediction': prediction})

@app.route('/chartdata', methods=['GET'])
def getchart_data():
    try:
        db = sqlite3.connect('mqtt_data.db')
        cursor = db.cursor()
        cursor.execute('SELECT timestamp, temperature, humidity, soil_humidity,soil_temperature, n, p, k FROM mqtt_data ')
        data = cursor.fetchall()

        result = []
        for row in data:
            result.append({
                'timestamp': row[0],
                'temperature': row[1],
                'humidity': row[2],
                'soil_humidity': row[3],
                'soil_temperature': row[4],
                'n' : row[5],
                'p' : row[6],
                'k' : row[7],
            })
        cursor.close()
        db.close()
        return jsonify(result)

    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/mqttdata', methods=['GET'])
def get_mqtt_data():
    return jsonify(mqtt_data)

User = "my-app-2000@ttn"
Password = "NNSXS.2SRZDRU5C6UD32MDHYKSFW7TFBOEGBKWNQESKCI.3EJOGRSVJ5TSGT7QP2M7FXEW7TNIQOYU577G2QX43QYLDOTWJB5Q"
theRegion = "EU1"
mqttc = mqtt.Client(client_id="1")
mqttc.on_connect = on_connect2
mqttc.on_message = on_message2
mqttc.username_pw_set(User, Password)
mqttc.tls_set()
mqttc.connect(theRegion.lower() + ".cloud.thethings.network", 8883, 60)
mqttc.subscribe("#", 0)
mqttc.loop_start()

mqttBrokerIp = "broker.hivemq.com"
mqttBrokerPort = 1883
mqttClient = mqtt.Client(client_id="2")

mqttClient.on_connect = on_connect1
mqttClient.on_message = on_message1

mqttClient.connect(mqttBrokerIp, mqttBrokerPort)

mqttClient.loop_start()

if __name__ == '__main__':
    app.run()