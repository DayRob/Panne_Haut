#include <Servo.h>;
Servo myservo;
#define servoPin 3;

int angle = 0;
int degre[5] = {0, 15, 20, 25,30,}; 
int degrre;
  
void setup() {
 myservo.attach(servoPin);
}


void loop() {

if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
    
delay(3598999);

if (degrre =0)
{
   myservo.write(0); 
   delay(1000); 
}

if (degrre =15)
{
   myservo.write(95); 
   delay(1000); {
}

if (degrre =20)
 {
   myservo.write(120); 
   delay(1000); 
}

if (degrre =25)
{
   myservo.write(150); 
   delay(1000); 
}

if (degrre =30)
   myservo.write(180); 
   delay(1000); 
}

}
}
