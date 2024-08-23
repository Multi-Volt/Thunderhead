/*
Copyright (c) 2024, John Simonis and The Ohio State University
This code was written by John Simonis for a research project at The Ohio State University.
*/
#include <Arduino.h>

//Here we define the pins we are going to use for the stepper driver, the relay for the electrolytes, and a pin for conducting each of our trials.
#define MistRelay 4
#define FirePin 5
#define HVPin 6
#define AirPin 7

//Times
#define MistingTime 2000
#define AirTime 1000
#define ArcTime 8000

//This is just a variable we use for keeping track of the time.
const int MotorPins[] = {8,9,10,11};
unsigned long LastTime = 0;
bool Firing = 0;


void setup() {
  pinMode(FirePin, INPUT_PULLUP); //This is the button we use for each shot
  pinMode(MistRelay, OUTPUT);
  ProbeStepper.setSpeed(60);q
  Serial.begin(9600);
  digitalWrite(Mistrelay, LOW);
  digitalWrite(HVPin, LOW);
}

void loop() {
  if (!Firing & !digitalRead(FirePin)){
    Firing = true;
    LastTime = millis();
    while((millis() < LastTime + MistingTime)){
      digitalWrite(MistRelay, HIGH);
    }
    LastTime = millis();
    digitalWrite(Mistrelay, LOW);
    digitalWrite(HVPin, HIGH);
  }
  if (firing){
  	while (millis() < (LastTime + AirTime)){	
    		digitalWrite(AirPin, HIGH);
    		digitalWrite(HVPin, HIGH);
  	}
  	LastTime = millis();
  	while (millis() < (LastTime + ArcTime)){
  		print("Flying...");
  		digitalWrite(HVPin, HIGH);
  	}
  	digitalWrite(HVPin, LOW);
  	Firing = false;
  }


}
