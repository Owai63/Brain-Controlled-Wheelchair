int button = 12;
int pot1 = A0;
int pot2 = A1;
int pot3 = A2;
int pot4 = A3;
int button1 = 2;
int button2 = 3;
int button3 = 4;
int button4 = 7;
float knob1;
float knob2;
float knob3;
float knob4;
float speed1;
float speed2;
char command;
bool modebt = 0;
bool up;
bool down;
bool left;
bool right;
int in1 = 5;
int in2 = 6;
int in3 = 9;
int in4 = 10;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
pinMode(in1,OUTPUT);
pinMode(in2,OUTPUT);
pinMode(in3,OUTPUT);
pinMode(in4,OUTPUT);
  pinMode(button,INPUT_PULLUP);
pinMode(pot1,INPUT);
pinMode(pot2,INPUT);
pinMode(pot3,INPUT);
pinMode(pot4,INPUT);
pinMode(button1,INPUT_PULLUP);
pinMode(button2,INPUT_PULLUP);
pinMode(button3,INPUT_PULLUP);
pinMode(button4,INPUT_PULLUP);
}




void loop() {
  // put your main code here, to run repeatedly:
  

// knob1 = analogRead(pot1);
// Serial.print("knob1");
// Serial.print(" ");
// Serial.println(knob1);
// knob2 = analogRead(pot2);
// Serial.print("knob2");
// Serial.print(" ");
// Serial.println(knob2);
// knob3 = analogRead(pot3);
// Serial.print("knob3");
// Serial.print(" ");
// Serial.println(knob3);
// knob4 = analogRead(pot4);
// Serial.print("knob4");
// Serial.print(" ");
// Serial.println(knob4);
// up =  digitalRead(button1);
// Serial.print("up");
// Serial.print(" ");
// Serial.println(up);
// down =  digitalRead(button2);
// Serial.print("down");
// Serial.print(" ");
// Serial.println(down);
// left =  digitalRead(button3);
// Serial.print("left");
// Serial.print(" ");
// Serial.println(left);
// right =  digitalRead(button4);
// Serial.print("right");
// Serial.print(" ");
// Serial.println(right);
// //delay(1000);

// speed1 = map(knob3,0,1023,0,255);
// Serial.print("speed1");
// Serial.print(" ");
// Serial.println(speed1);
// speed2 = map(knob4,0,1023,0,255);  
// Serial.print("speed2");
// Serial.print(" ");
// Serial.println(speed2);

//delay(1000);
Serial.println(command);
//Stop();
if(digitalRead(button) == 0){
  modebt = 1;
}
if(digitalRead(button) == 1){
  modebt = 0;
}
if (modebt == 1){


    switch(command){
    case 'F':  
      forward();
      break;
    case 'B':  
       backward();
      break;
    case 'L':  
      Left();
      break;
    case 'R':
      Right();
      break;
    
    }}

    
   


else {
  if (knob1>550 || up == 0){
  
  forward();
  
  
  }


  else if (knob1<450 || down == 0){
  
  backward();
  
  
  }

  else if (knob2>550 || right == 0){
  
  Right();
  
  
  }


  else if (knob2<450 || left == 0){
  
  Left();
  
  
  }
  else {
    Stop();
    }



}
}





void forward(){
  analogWrite(in1,speed1);
  analogWrite(in2,0);
  analogWrite(in3,speed2);
  analogWrite(in4,0);
  
  
  }


  void backward(){
  analogWrite(in1,0);
  analogWrite(in2,speed1);
  analogWrite(in3,0);
  analogWrite(in4,speed2);
  
  
  }


  void Left(){
  analogWrite(in1,speed1);
  analogWrite(in2,0);
  analogWrite(in3,0);
  analogWrite(in4,speed2);
  
  
  }


  void Right(){
  analogWrite(in1,0);
  analogWrite(in2,speed1);
  analogWrite(in3,speed2);
  analogWrite(in4,0);
  
  
  }


  void Stop(){
  analogWrite(in1,0);
  analogWrite(in2,0);
  analogWrite(in3,0);
  analogWrite(in4,0);
  
  
  }
