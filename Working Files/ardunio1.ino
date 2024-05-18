#include <Wire.h>
#include <Adafruit_MLX90614.h>

const int hallSensorPin = A0; // Pin for the Hall effect sensor
const int magnetThreshold = 100; // Threshold to detect the magnet
int magnetPassCounter = 0; // Counter for the number of times the magnet passes
Adafruit_MLX90614 mlx = Adafruit_MLX90614(); // Creates the IFR Sensor and establishes it

void setup() {
  Serial.begin(4800); //Sets up Serial Monitor for Arduino 1
  mlx.begin(); // Initialize the MLX90614 sensor
  pinMode(hallSensorPin, INPUT);
}

void loop() {
  int sensorValue = analogRead(hallSensorPin);
  
  // Checks to see if the magnet is close to the hall effect sensor
  if (sensorValue < magnetThreshold) {
    magnetPassCounter++;
    while(analogRead(hallSensorPin) < magnetThreshold) {
      // Wait for the magnet to pass completely
    }
  }

  // Read the object temperature from the MLX90614 sensor
  float objectTemp = mlx.readObjectTempF();
  
  // Print both speed and object temperature in one line which allows pyserial to read
  
  Serial.print(magnetPassCounter);
  Serial.print(" ");
  Serial.println(objectTemp);

  delay(500);
}