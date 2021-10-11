# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
#
# name:pirobo
# Author:jh1cdv
# date:2017/07/02
# input sensor1,2
# process input to output -0.5 +0.5
# output: rotationserbo

import RPi.GPIO as GPIO
from time import sleep


#from __future__ import division
#import time
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685
import paho.mqtt.client as mqtt
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit

import json


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
myMotor1 = mh.getMotor(1)
myMotor2 = mh.getMotor(2)

Vspeed = 150

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    pwm = Adafruit_PCA9685.PCA9685(0x60)

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #print(str(msg.payload))
    r = (str(msg.payload))
    print(r)
    #b'{"topic":"In-ch0-7","payload":{"ch1":0,"ch0":0},"qos":2,"retain":false,"_topic":"In-ch0-7"}'
    r1=r.replace("b'","")
    r1=r1.replace("'","")
    r1=r1.replace("In-ch0-7","In")
    
    print(r1)
    #{"topic":"In-ch0-7","payload":{"ch1":0,"ch0":0},"qos":2,"retain":false,"_topic":"In-ch0-7"}

    
    #r1 = json.loads(msg.payload) #TypeError
    r2 = json.loads(str(r1))
    print(r2)
    #{'payload': {'ch0': 0, 'ch1': 0}, '_topic': 'In-ch0-7', 'topic': 'In-ch0-7', 'qos': 2, 'retain': False}

    
    r3 = json.dumps(r2)
    print(r3)
    #{"payload": {"ch0": 0, "ch1": 0}, "_topic": "In-ch0-7", "topic": "In-ch0-7", "qos": 2, "retain": false}

    #print("topic=",r2['topic'])  #keyError:'ch0'
    #print("payload=",r2['payload']['ch0'])  #keyError:'ch0'
    
    print("ch0=",r2["ch0"])  #keyError:'ch0'
#b'{"ch2":4093,"ch4":0,"ch3":0,"ch0":0,"ch7":1278,"ch5":0,"ch1":4094,"ch6":0}'
#{"ch2":4093,"ch4":0,"ch3":0,"ch0":0,"ch7":1278,"ch5":0,"ch1":4094,"ch6":0}
#{'ch3': 0, 'ch4': 0, 'ch2': 4093, 'ch1': 4094, 'ch5': 0, 'ch0': 0, 'ch7': 1278, 'ch6': 0}
#{"ch3": 0, "ch4": 0, "ch2": 4093, "ch1": 4094, "ch5": 0, "ch0": 0, "ch7": 1278, "ch6": 0}
#ch0= 0
    #pwm.set_pwm(0, 4096-r2["ch0"],r2["ch0"])
    #pwm.set_pwm(1, 4096-r2["ch1"],r2["ch1"])
    #pwm.set_pwm(2, 4096-r2["ch2"],r2["ch2"])
    #pwm.set_pwm(3, 4096-r2["ch3"],r2["ch3"])
    #pwm.set_pwm(4, 4096-r2["ch4"],r2["ch4"])
    #pwm.set_pwm(5, 4096-r2["ch5"],r2["ch5"])
    #pwm.set_pwm(6, 4096-r2["ch6"],r2["ch6"])
    #pwm.set_pwm(7, 4096-r2["ch7"],r2["ch7"])
    V4 = r2["ch6norm"]
    
    V4 *= 70 #    V4 *= 156 
    V4 += 185
    V4 = int(V4)
    #pwm.set_pwm(6, 4096-V4, V4)

    V5 = r2["ch7norm"]
    
    V5 *= 70 #   V5 *= 156 
    V5 += 185
    V5 = int(V5)
    #pwm.set_pwm(7, 4096-V5, V5)


    V6 = float(r2["ch6norm"])
    print("V6="+str(V6))
    if 0 < V6 or V6 == 0: #1200 < V6 < 1600:
        Vspeed = V6 
        Vspeed *= 300 
        
        print("M1 Forward! "+str(V6)+str(int(Vspeed)))
        myMotor1.setSpeed(int(Vspeed))
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
    if  V6 < 0: #800 < V6 < 1200: 
        Vspeed = V6 
        Vspeed *= -1
        Vspeed *= 300 
        
        print("M1 BACKWARD! "+str(V6)+str(int(Vspeed)))
        myMotor1.setSpeed(int(Vspeed))
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        
    V7 = float(r2["ch7norm"])
    print("V7="+str(V7))
    if 0 < V7 or V7 == 0: #1200 < V6 < 1600:
        Vspeed = V7 
        Vspeed *= 300 
        
        print("M2 Forward! "+str(V7)+str(int(Vspeed)))
        myMotor2.setSpeed(int(Vspeed))
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
    if  V7 < 0: #800 < V6 < 1200: 
        Vspeed = V7 
        Vspeed *= -1
        Vspeed *= 300 
        
        print("M2 BACKWARD! "+str(V7)+str(int(Vspeed)))
        myMotor2.setSpeed(int(Vspeed))
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
 

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)



# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685(0x60)

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 0  # Min pulse length out of 4096 0 150
servo_max = 600  # Max pulse length out of 4096 1 600

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    print('{0}pulse'.format(pulse))
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
#pwm.set_pwm_freq(60)
#pwm.set_pwm_freq(50)
# input -0.5 ---   0 ----  +0.5
#        102   ---297  ----492  195/390/4096
#v = 0
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("Out-ch0-7",0)

mqttc.loop_start()


try:
    while True:
     if __name__ == '__main__':
         
        #v1 = 4095.0
        v1 = 100.0
        #v1 = 48.0
        #v1 = 0



        v = int(v1)
        
        #pwm.setDutyCycle(0,0.25)
        if v > 4096:
            v = 0
        #pwm.set_pwm(0, 0, 10)
        #pwm.set_pwm(2, 0, 4096)
        #pwm.set_pwm(4, 4096-v, v)
        #pwm.set_pwm(6, 4096-v, v)

        v = int(v1)
        if v > 4096:
            v = 0
        #pwm.set_pwm(1, 0, 2048)
            #pwm.set_pwm(3, 4096-v, v)
            #pwm.set_pwm(5, 4096-v, v)
        #pwm.set_pwm(7, 4096-v, v)


        #time.sleep(1)
        # Initialise the PCA9685 using the default address (0x40).
        pwm = Adafruit_PCA9685.PCA9685(0x60)

        
        sleep(1.10)
except KeyboardInterrupt:
    pass
#f.close()
GPIO.cleanup()
