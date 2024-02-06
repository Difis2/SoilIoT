#include <DHT.h>

#define DHTPIN 3  // Digital pin connected to the DHT22
#define DHTTYPE DHT22  // Change this if you're using a different DHT sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);  // Delay for 2 seconds

  float temperature = dht.readTemperature();  // Read temperature in Celsius
  float humidity = dht.readHumidity();  // Read humidity

  // Check if any reads failed
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C\tHumidity: ");
  Serial.print(humidity);
  Serial.println(" %");
}
