# Resume
Nowadays, the conditions of climate change, prolonged drought and decreasing of crops field due to the exponential increase of the population, agriculture needs a more sustainable approach. Solutions that meet sustainability are associated with precision agriculture. In this context, the objective assessment of soil conditions and mapping using geographic information systems is of the utmost importance. So, the measurement of the concentration of nutrients in the soil such as nitrogen, phosphorus or potassium as well as moisture and temperature are essential for controlling the level of wat stress and nutrient stress that allows a great production efficiency. Internet of Things solutions that are represented by sensor networks for monitoring soil characteristics with or without contact are characterized by LoRa, Wi-Fi type communication protocols and NB-IoT. The sensor data are useful for the development of very useful predictive models for the availability of nutrients and the optimization of water management, being considered also the most important actuators in the optimal administration of water and nutrients. Therefore, this project proposal arises, which aims to develop an IoT ecosystem for precision agriculture. In this project, three major parts of the IoT system were carried out: the base of the project, which consists of obtaining data from sensors and subsequently sending them to the server, a server that receives, processes and stores the data in a database and finally the website, for data visualization and analysis.

# Hardware
- Waterproof capacitive soil moisture v2.0
- Waterproof Digital Thermometer DS18B2
- Temperature-humidity sensor DHT22
- NPK sensor
- The Things Gateway
- Dragino LoRa/GPS shield
- Dragino Gateway LG01-N
- Arduino UNO

<p align="center">
        <img src="https://github.com/Difis2/SoilIoT/assets/123119639/8fccf180-3614-4bac-bdc0-0acbdbd01038" />
</p>

  <p align="center">
        <img src="https://github.com/Difis2/SoilIoT/assets/123119639/4c7f8267-5cf2-4c45-9b63-73f3b6ceafa0" />
</p>



# Software
- Python
- HTML, CSS and JavaScript
- Arduino IDE
- SQLite
- Jupyter

<p align="center">
        <img src="https://github.com/Difis2/SoilIoT/assets/123119639/5cbcc13d-3496-4ba4-b3f0-af6d73f58670" />
</p>


# Overview of the ecosystem

We have 2 groups of sensors: LoRa communication group , LoRaWan communication group. This was not the optimal way, but it was the only way due to the communication support between LoRaWan and dragino gateway to not be possible to communicate between each other, so we add another gateway TTN gateway to help resolve this issue. After sending the data via LoRa or LoRaWan, the gateways publish that data via MQTT to each broker, TTN broker and Hivemq broker, a free broker that can be used.<br />

After the publish, the server will subscribe to both topics and receive the data from the sensor, for visualization in real time or to store data for later analysis. But before all of this, a prediction model was created with the help of [CropRecommendation database](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset). This model will be used to predict the best crop for our sensor data, to some characteristics like Nitrogen, Potassium, Phosphorus, temperature and humidity. This prediction is made with the help of an API that send the data to the server so it can get a result.<br />

To see the data in real time (30 minutes of interval, because the npk sensor only get data with a 30 minutes intervals), we wait for both sensors to send the data, and after that we have APIs programmed to send that data to our website. The next dashboard should appear if everything is working.

<p align="center">
        <img src="https://github.com/Difis2/SoilIoT/assets/123119639/fc3df96e-c9dd-444f-995c-95478ee3b563" />
</p>




