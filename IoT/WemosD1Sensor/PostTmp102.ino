#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h> // Used to establied serial communication on the I2C bus
#include <SparkFunTMP102.h> // Used to send and recieve specific information from our sensor

const char* ssid = "change";
const char* password = "change";

DynamicJsonDocument postData(256);
TMP102 sensor0;

void setup() 
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(1000);
    Serial.println("Connecting...");
  }

  Wire.begin(); //Join I2C Bus
  
  if(!sensor0.begin())
  {
    Serial.println("Cannot connect to TMP102.");
    Serial.println("Is the board connected? Is the device ID correct?");
    while(1);
  }
  
  Serial.println("Connected to TMP102!");
  delay(100);

  // set the Conversion Rate (how quickly the sensor gets a new reading)
  //0-3: 0:0.25Hz, 1:1Hz, 2:4Hz, 3:8Hz
  sensor0.setConversionRate(2);
  
  //set Extended Mode.
  //0:12-bit Temperature(-55C to +128C) 1:13-bit Temperature(-55C to +150C)
  sensor0.setExtendedMode(0);
}

void loop() 
{
  float temperature;
  
  // Turn sensor on to start temperature measurement.
  // Current consumtion typically ~10uA.
  sensor0.wakeup();

  // read temperature data
  temperature = sensor0.readTempF();
  //temperature = sensor0.readTempC();

  // Place sensor in sleep mode to save power.
  // Current consumtion typically <0.5uA.
  sensor0.sleep();
  
  if (WiFi.status() == WL_CONNECTED) 
  {
    postData["sensorName"] = "practice";
    postData["temp"] = temperature;

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