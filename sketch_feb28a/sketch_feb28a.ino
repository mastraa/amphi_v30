struct Mvicb_t { //NMEA: Mètis Vela Infusion Check Byte
  byte tipo;
  unsigned long times;
  float ext_t, ext_u, inl_t, oul_t, ins_t;
};

struct Mvupcb_t //NMEA: Mètis Vela UniPd Corta Byte
{
    byte tipo;
    long lat,lon;
    unsigned long gradi, date, times;
    float vel, attitude[3];
};

struct Mvupb_t //NMEA: Mètis Vela UniPd Byte
{
    byte tipo;
    long lat,lon;
    unsigned long gradi, date, times;
    float vel, attitude[3], tempDS, left, right;
    byte Wspeed, vale_1, vale_2;
    };

typedef struct Mvicb_t Mvic;
typedef struct Mvupb_t Mvup;
typedef struct Mvupcb_t Mvupc;

Mvic mvic;
Mvup mvup;

byte * c = (byte *) &mvup;
byte * b = (byte *) &mvic;



void setup() {
  Serial.begin(57600);
  //Serial.println(sizeof(Mvupb_t));
  pinMode(13, OUTPUT);
  mvup.tipo=7;
  mvup.lat=1111543456;
  mvup.lon=2111543457;
  mvup.gradi=10666;
  mvup.date=2111543438;
  mvup.times=millis();
  mvup.vel=10.49;
  mvup.attitude[0]=17.65;
  mvup.attitude[1]=95.65;
  mvup.attitude[2]=110.76;
  mvup.tempDS=26.51;
  mvup.left=56.12;
  mvup.right=65.78;
  mvup.Wspeed=10;
  mvup.vale_1=1;
  mvup.vale_2=245;

  
  mvic.tipo=10;
  mvic.times=millis();
  mvic.ext_t=-11.75;
  mvic.ext_u=10.40;
  mvic.inl_t=89.10;
  mvic.oul_t=-10.00;
  mvic.ins_t=11.45;
}

void loop() {
  mvup.attitude[0]=randNum();
  mvup.attitude[1]=randNum();
  mvup.attitude[2]=randNum();
  mvup.times=millis();
  //mvic.times=millis();
  sendStruct(c, sizeof(Mvupb_t), '$', '\n');
  //sendStruct(b, sizeof(Mvicb_t), '$', '\n');
  delay(1000);
}


void sendStruct(byte* commands, byte len, byte starter, byte ender){//send command
  byte _XOR;
  Serial.write(starter);
  for (byte i=0; i<len; ++i){
    Serial.write(commands[i]);
  }
  Serial.write('*');
  _XOR = getCheckSum(commands, len);
  Serial.write(_XOR);
  Serial.write(ender);
}

void sendCommand(byte type, byte* commands, byte len, byte starter, byte ender){//send command
    byte _XOR;
    Serial.write(starter);
    Serial.write(type);
    //Serial.print(",");//separatore, per i byte non  serve
    for (byte i=0; i<len; ++i){
        Serial.write(commands[i]);
    }
    Serial.write('*');
    _XOR = type^getCheckSum(commands, len);
    Serial.write(_XOR);
    Serial.write(ender);
}

uint8_t getCheckSum(char *string){//checksum for string type
    int XOR = 0;
    for (int i = 0; i < strlen(string); i++)
    {
        XOR = XOR ^ string[i];
    }
    return XOR;
}

uint8_t getCheckSum(byte *buff, int l){//checksum for byte type
    uint8_t XOR = 0;
    for (int i=0; i<l; ++i){
        XOR = XOR^buff[i];
    }
    return XOR;
}

float randNum(){
  float num=(float)(rand()/100+5);
  if (num>360){
   num=num-(num-360+50.43);
  }
  return num; 

}
