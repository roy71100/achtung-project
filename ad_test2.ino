#define BACK 13
#define FORWARD 12
#define RIGHT 11
#define LEFT 10
#define B_KEY 1
#define F_KEY 2
#define L_KEY 3
#define R_KEY 4
#define B_R_KEY 5
#define F_R_KEY 6
#define L_R_KEY 7
#define R_R_KEY 8
#define DELAY 100

//CODE_DOCT={"B":1,"F":2,"L":3,"R":4,"B_R":5,"F_R":6,"L_R":7,"R_R":8}

void setup() {
  Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
  pinMode(FORWARD,OUTPUT);
  pinMode(BACK,OUTPUT);
  pinMode(RIGHT,OUTPUT);
  pinMode(LEFT,OUTPUT);
}

void loop() {
  char inByte = ' ';
  if(Serial.available()){ // only send data back if data has been sent
     char inByte = Serial.read();// read the incoming data
     if (inByte == L_KEY){
      digitalWrite(LEFT,HIGH);
     }
     
     if (inByte == R_KEY){
      digitalWrite(RIGHT,HIGH);
     }
    
     if (inByte == F_KEY){
      digitalWrite(FORWARD,HIGH);
     }
     
     if (inByte == B_KEY){
      digitalWrite(BACK,HIGH);
     }
     
     if (inByte == B_R_KEY){
      digitalWrite(BACK,LOW);
     }
     
     if (inByte == F_R_KEY){
      digitalWrite(FORWARD,LOW);
     }

     if (inByte == L_R_KEY){
      digitalWrite(LEFT,LOW);
     }

     if (inByte == R_R_KEY){
      digitalWrite(RIGHT,LOW);
     }
  }
}
 
