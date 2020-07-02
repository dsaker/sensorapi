#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include "DHTesp.h" //https://github.com/beegee-tokyo/DHTesp

const char* ssid = "";
const char* password = "";

DynamicJsonDocument postData(256);

void setup() 
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(1000);
    Serial.println("Connecting...");
  }

  //setup DHT22 sensor
  dht.setup(D2, DHTesp::DHT22);
  

}

void loop() 
{
  float humidity = dht.getHumidity();
  float temperature = dht.getTemperature();
  float F = dht.toFahrenheit(temperature);
  
  if (WiFi.status() == WL_CONNECTED) 
  {
    postData["sensorName"] = "practice";
    postData["temp"] = F;
    postData["humidity"] = humidity;

    String json; 
    serializeJson(postData, json);

    HTTPClient http; //Object of class HTTPClient
    http.begin("http://192.168.1.121:5000/api");

    int httpCode = http.POST(json);

    Serial.println(http.getString());

    http.end(); //Close connection
  }
  
  delay(6000);
}