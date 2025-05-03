// Pi-5 Input Pins 
#define Pi_pin1 D1
#define Pi_pin2 D2
#define Pi_pin3 D4
// Frequency Output Pin 
#define freq D5

void setup() {
  // put your setup code here, to run once:
  pinMode(Pi_pin1, INPUT);
  pinMode(Pi_pin2, INPUT);
  pinMode(Pi_pin3, INPUT);
  pinMode(freq, OUTPUT);
}

int setFreq() {
  bool P1 = digitalRead(Pi_pin1);
  bool P2 = digitalRead(Pi_pin2);
  bool P3 = digitalRead(Pi_pin3);
  int f;
  if (P1 == 0 && P2 == 0 && P3 == 1 )
    f = 100;
  else if (P1 == 0 && P2 == 1 && P3 == 0 )
    f = 200;
  else if (P1 == 0 && P2 == 1 && P3 == 1 )
    f = 300;
  else if (P1 == 1 && P2 == 0 && P3 == 0 )
    f = 400;
  else if (P1 == 1 && P2 == 0 && P3 == 1 )
    f = 500;
  return f;
  }
void loop() {
  // put your main code here, to run repeatedly:
  int Freq = setFreq();
  analogWriteFreq(Freq);
  analogWrite(freq, 128);
}
