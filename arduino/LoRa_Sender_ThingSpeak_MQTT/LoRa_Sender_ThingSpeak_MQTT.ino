/*
  LoRa_Sender_MQTT:
  Support Devices: LoRa Shield + Arduino 
  
  Require Library:
  https://github.com/sandeepmistry/arduino-LoRa 
  
  Example sketch showing how to send or a message base on ThingSpeak(https://thingspeak.com) MQTT format. 
  The End node will send out a string "<End_Node_ID>field1=${TEMPERATURE_VALUE}&field2=${HUMIDITY_VALUE}" to LG01/LG02 gateway. 
  When the LG01/LG02 gateway get the data, it will parse and forward the data to ThingSpeak via MQTT protocol. 
  modified Dec 26 2018
  by Dragino Technology Co., Limited <support@dragino.com>
*/

#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 4
#define DHTPIN 3  
#define DHTTYPE DHT22  

DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);


int count=0;
int device_id=5679; 


void setup() {
  Serial.begin(9600);
  //while (!Serial);
    dht.begin();
    sensors.begin();
  Serial.println("LoRa Sender");
  if (!LoRa.begin(868000000)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setSyncWord(0x34);
}

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(count);
  float temp = dht.readTemperature();  // Read temperature in Celsius
  float hum = dht.readHumidity();  // Read humidity
  int soilhum = analogRead(A0);  // Read soil humidity
  float soiltemp = sensors.getTempCByIndex(0); // Read soil temperature
  Serial.println(soiltemp);
  // compose and send packet
  LoRa.beginPacket();
  LoRa.print("<");
  LoRa.print(device_id);
  LoRa.print(">temp=");
  LoRa.print(temp);
  LoRa.print("&hum=");
  LoRa.print(hum); 
  LoRa.print("&soilhum=");
  LoRa.print(soilhum); 
  LoRa.print("&soiltemp=");
  LoRa.print(soiltemp);
 // LoRa.print(counter);
  LoRa.endPacket();
  count++;
  delay(1800000);
}
