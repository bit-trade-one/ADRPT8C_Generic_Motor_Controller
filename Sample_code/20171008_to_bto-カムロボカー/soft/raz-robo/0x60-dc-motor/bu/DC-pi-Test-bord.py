#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
#mh = Adafruit_MotorHAT(addr=0x60)
mh = Adafruit_MotorHAT(addr=0x70)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
#myMotor = mh.getMotor(1)
#myMotor = mh.getMotor(3)
myMotor = mh.getMotor(1)
myMotor2 = mh.getMotor(2)


# set the speed to start, from 0 (off) to 255 (max speed)
#myMotor.setSpeed(150)
#myMotor.run(Adafruit_MotorHAT.FORWARD);
# turn on motor
#myMotor.run(Adafruit_MotorHAT.RELEASE);
#    myMotor.run(Adafruit_MotorHAT.BACKWARD)

while (True):
    print("Forward! ")
    myMotor.setSpeed(150)
    myMotor.run(Adafruit_MotorHAT.FORWARD)
    
    myMotor2.setSpeed(150)
    myMotor2.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(1.0)

    print("BACKWARD")
    myMotor.setSpeed(150)
    myMotor.run(Adafruit_MotorHAT.BACKWARD)
    myMotor2.setSpeed(150)
    myMotor2.run(Adafruit_MotorHAT.BACKWARD)
    time.sleep(1.0)

 
    print("Release")
    myMotor.run(Adafruit_MotorHAT.RELEASE)
    time.sleep(1.0)
