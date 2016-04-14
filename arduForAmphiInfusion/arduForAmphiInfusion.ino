#include <math.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN            2         // Pin which is connected to the DHT sensor.
#define DHTTYPE           DHT11     // DHT 11


float k;
float R1=10000.0;


void setup() {
  Serial.begin(57600);
  Serial.println("R[Ohm] \t t[°C]");
  // put your setup code here, to run once:

}

void loop() {
  int dv_1=analogRead(A15);
  float Rx=R1*(1024-dv_1)/dv_1;
  float t = -22.62*log(Rx)+233.67;
  Serial.print(Rx);
  Serial.print('\t');
  Serial.println(t);
  
  delay(1000);
  // put your main code here, to run repeatedly:

}
