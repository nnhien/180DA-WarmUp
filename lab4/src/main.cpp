#include <Arduino.h>
#include <ArduinoMqttClient.h>
#include <Arduino_LSM6DS3.h>
#include <WiFiNINA.h>
#include <ArduinoJson.h>

#include "arduino_secrets.h"

const char MQTT_BROKER[] = "broker.hivemq.com";
const char MQTT_TOPIC[] = SECRET_TOPIC;
const int  MQTT_PORT = 1883;

int wifi_status = WL_IDLE_STATUS;

char WIFI_SSID[] = SECRET_SSID;
char WIFI_PASS[] = SECRET_PASS;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

float ax, ay, az;
float gx, gy, gz;

JsonDocument mqttMsg;

void setup() {
    Serial.begin(9600);
    while (!Serial);

    Serial.println("Arduino IMU over MQTT");
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU");
        while(1);
    }
    Serial.println("Initialized IMU");
    Serial.print("Gyroscope sample rate = ");
    Serial.print(IMU.gyroscopeSampleRate());
    Serial.println(" Hz");

    Serial.print("Accelerometer sample rate = ");
    Serial.print(IMU.accelerationSampleRate());
    Serial.println(" Hz");

    Serial.print("Attempting to connect to SSID: ");
    Serial.print(WIFI_SSID);
    int wifi_attempts = 0;
    while (WiFi.begin(WIFI_SSID, WIFI_PASS) != WL_CONNECTED && wifi_attempts < 5) {
        wifi_attempts++;
        Serial.print(".");
        delay(500);
    }
    if (wifi_attempts == 5) {
        Serial.println("Reached maximum wifi connection attempts");
        while(1);
    }
    Serial.println();
    Serial.println("Connected to WiFi");

    Serial.print("Attempting to connect to MQTT broker: ");
    Serial.println(MQTT_BROKER);
    if (!mqttClient.connect(MQTT_BROKER, MQTT_PORT)) {
        Serial.print("Failed to connect to MQTT broker");
        while(1);
    }
    Serial.println("Connected to MQTT broker");
}

void loop() {
    mqttClient.poll();

    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(gx, gy, gz);
    } 
    if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(ax, ay, az);
    }

    mqttClient.beginMessage(MQTT_TOPIC);
    mqttMsg["ax"] = ax;
    mqttMsg["ay"] = ay;
    mqttMsg["az"] = az;
    mqttMsg["gx"] = gx;
    mqttMsg["gy"] = gy;
    mqttMsg["gz"] = gz;
    serializeJson(mqttMsg, mqttClient);
    mqttClient.endMessage();
    delay(50);
}