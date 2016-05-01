#include <math.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Mille_UNO.h>


#define DHTTYPE           DHT11     // DHT 11

//PIN DEFINE
#define DHTPIN            2         // Pin which is connected to the DHT sensor.
#define INLET             0
#define SAVELED           4
#define SAVEBTN           3


DHT_Unified dht(DHTPIN, DHTTYPE);
float k;
float R1=10000.0;
uint32_t delayMS;
bool save = 0;

typedef struct Mvic_t mvic_t;
mvic_t mvic;

void setup() {
  Serial.begin(57600);
  Serial.println("\n est_t[°C] \t est_u[%] \t inl_t[°C] \t out_t[°C] \t ins_t[°C]");
  dht.begin();
  sensor_t sensor;
  delayMS = sensor.min_delay / 1000;
  pinMode(SAVELED, OUTPUT);
  pinMode(SAVEBTN, INPUT);
  attachInterrupt(digitalPinToInterrupt(SAVEBTN), ISR_FUNC, RISING);
  // put your setup code here, to run once:

}

void loop() {
  delay(1000);
  
  int dv_1=analogRead(INLET);
  float Rx=R1*(1024-dv_1)/dv_1;
  mvic.inl_t = -22.62*log(Rx)+233.67;


  // Get temperature event and print its value.
  sensors_event_t event;  
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    mvic.ext_t=0;
    mvic.ext_u=0;
  }
  else {
    mvic.ext_t=event.temperature-1.5;
    dht.humidity().getEvent(&event);
    mvic.ext_u=event.relative_humidity;
  }
  printMVIC(mvic);
}

void ISR_FUNC(){
  save=!save;
  digitalWrite(SAVELED, save);
}

void printMVIC(struct Mvic_t data){
  Serial.print(mvic.ext_t);Serial.print('\t');
  Serial.print(mvic.ext_u);Serial.print('\t');
  Serial.print(mvic.inl_t);Serial.print('\t');
  Serial.print(mvic.oul_t);Serial.print('\t');
  Serial.print(mvic.ins_t);Serial.print('\n');
}


