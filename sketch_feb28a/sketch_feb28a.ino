
float temp[6];
byte * b = (byte *) &temp;

struct mvic { 
byte tipo;
float ext_t;
float ext_u;
float inl_t;
float oul_t;
float ins_t;
}; 

typedef struct mvic t_mvic;

t_mvic Mvic;

byte * c = (byte *) &Mvic;



void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  temp[0]=-11.75;
  temp[1]=10.40;
  temp[2]=89.10;
  temp[3]=-10.00;
  temp[4]=11.45;
}

void loop() {
  //Serial.write(prova);
  //Serial.write(array,4);
  //Serial.write(buf,4);
  //Serial.write('\n');
  sendCommand(10, b, 20, '$', '\n');
  sendStruct(c, sizeof(mvic), '$', '\n'); 
  delay(1000);
}


void sendStruct(byte* commands, byte len, byte starter, byte ender){//send command
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
