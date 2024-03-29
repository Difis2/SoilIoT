#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>
// This is the LoRa Node side sketch for the MQTT example: http://wiki.dragino.com/index.php?title=MQTT_Forward_Instruction#Example_to_communicate_to_a_simple_MQTT_server 


#define DHTPIN 3  // Digital pin connected to the DHT22
#define DHTTYPE DHT22  // Change this if you're using a different DHT sensor

DHT dht(DHTPIN, DHTTYPE);
float tem,hum;
char tem_1[8]={"\0"},hum_1[8]={"\0"};   
char *node_id = "<5679>";  //From LG01 via web Local Channel settings on MQTT.Please refer <> dataformat in here. 
uint8_t datasend[36];
unsigned int count = 1; 
unsigned long new_time,old_time=0;

void setup()
{
      Serial.begin(9600);
      dht.begin();
      while (!Serial);
      Serial.println(F("Start MQTT Example"));
      if (!LoRa.begin(868000000))   //868000000 is frequency
      { 
          Serial.println("Starting LoRa failed!");
          while (1);
      }
      // Setup Spreading Factor (6 ~ 12)
      LoRa.setSpreadingFactor(7);
      
      // Setup BandWidth, option: 7800,10400,15600,20800,31250,41700,62500,125000,250000,500000
      //Lower BandWidth for longer distance.
      LoRa.setSignalBandwidth(125000);
      
      // Setup Coding Rate:5(4/5),6(4/6),7(4/7),8(4/8) 
      LoRa.setCodingRate4(5);
      LoRa.setSyncWord(0x34); 
      Serial.println("LoRa init succeeded.");
      
      LoRa.onReceive(onReceive);   
      LoRa.receive();     
}

void dhtTem()
{
       tem = dht.readTemperature();  // Read temperature in Celsius     
       hum = dht.readHumidity();  // Read humidity             
       Serial.println(F("The temperature and humidity:"));
       Serial.print("[");
       Serial.print(tem);
       Serial.print("℃");
       Serial.print(",");
       Serial.print(hum);
       Serial.print("%");
       Serial.print("]");
       Serial.println("");
}
void dhtWrite()
{
    char data[50] = "\0";
    for(int i = 0; i < 50; i++)
    {
       data[i] = node_id[i];
    }

    dtostrf(tem,0,1,tem_1);
    dtostrf(hum,0,1,hum_1);

    // Serial.println(tem_1);
     strcat(data,"tem=");
     strcat(data,tem_1);
     strcat(data,"&hum=");
     strcat(data,hum_1);
     strcpy((char *)datasend,data);
     
   //Serial.println((char *)datasend);
    //Serial.println(sizeof datasend);
      
}


void SendData()
{
     LoRa.beginPacket();
     LoRa.print((char *)datasend);
     LoRa.endPacket();
     Serial.println("Packet Sent");
}    
    


void loop()
{
    new_time=millis();
    if (new_time - old_time >= 60000 || old_time == 0)
    {
      old_time = new_time;
      Serial.print("###########    ");
      Serial.print("COUNT=");
      Serial.print(count);
      Serial.println("    ###########");
      count++;
      dhtTem();
      dhtWrite();
      SendData();
      LoRa.receive();
    }
}

void onReceive(int packetSize) {
 
  // received a packet
  Serial.print("Received packet : ");

  // read packet
  for (int i = 0; i < packetSize; i++) {
      Serial.print((char)LoRa.read());
  }
  Serial.print("\n\r");  
}
