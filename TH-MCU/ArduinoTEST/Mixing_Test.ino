/*
Copyright (c) 2023, John Simonis and The Ohio State University
This code was written by John Simonis for a research project at The Ohio State University.
*/
#include <Arduino.h>
#include <Stepper.h>

//Here we define the pins we are going to use for the stepper driver, the relay for the electrolytes, and a pin for conducting each of our trials.
#define MistRelay 4
#define TrialPin 5
#define HVPin 6

//Times
#define MistingTime 2000
#define ArcTime 1000

//This is just a variable we use for keeping track of the time.
const int MotorPins[] = {8,9,10,11};
unsigned long LastTime = 0;
bool TrialIP = 0;


//Defining a stepper object with our preset pins and 200 steps per revolution.
Stepper ProbeStepper(200, MotorPins[0], MotorPins[1], MotorPins[2], MotorPins[3]);

void setup() {
  pinMode(TrialPin, INPUT_PULLUP); //This is the button we use for each trials
  pinMode(MistRelay, OUTPUT);
  ProbeStepper.setSpeed(60);q
  Serial.begin(9600);
  digitalWrite(Mistrelay, LOW);
  digitalWrite(HVPin, LOW);
}

void loop() {
  if (!TrialIP & !digitalRead(TrialPin)){
    TrialIP = true;
    ProbeStepper.step(200); //400 steps/mm so step half a mm
    LastTime = millis();
    while((millis() < LastTime + MistingTime)){
      digitalWrite(MistRelay, HIGH);
    }
    LastTime = millis();
      digitalWrite(Mistrelay, LOW);
      digitalWrite(HVPin, HIGH);
  }
  if (millis() > (LastTime + ArcTime)){
    TrialIP = false;
    digitalWrite(HVPin, LOW);
  }


}
