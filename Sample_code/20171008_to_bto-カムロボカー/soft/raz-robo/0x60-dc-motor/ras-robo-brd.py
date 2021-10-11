#!/usr/bin/python
# v1.0 2017/7/28 jh1cdv 自律動作　動作確認ＯＫ
# Input:MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
# Output: -0.5 --- 0 --- +0.5
#        mqtt topic=/In-ch0,1
#


import RPi.GPIO as GPIO
from time import sleep

import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)



# MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    adcout = 0
    adcout = 0  
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout

GPIO.setmode(GPIO.BCM)
# ピンの名前を変数として定義
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8
# SPI通信用の入出力を定義
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)
#f = open("/var/tmp/mcp3208-ch0.txt","w")
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()


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

# set the speed to start, from 0 (off) to 255 (max speed)
#myMotor.setSpeed(150)
#myMotor.run(Adafruit_MotorHAT.FORWARD);
# turn on motor
#myMotor.run(Adafruit_MotorHAT.RELEASE);
#    myMotor.run(Adafruit_MotorHAT.BACKWARD)

while (True):
    inputVal6 = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
    V6 = float(inputVal6)
    print("V6="+str(V6))
    if 1200 < V6 < 4095: #1200 < V6 < 1600:
        Vspeed = V6 - 1200
        Vspeed /= 3 
        
        print("M1 Forward! "+str(V6)+str(int(Vspeed)))
        myMotor1.setSpeed(int(Vspeed))
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
    if 0 < V6 < 1200: #800 < V6 < 1200: 
        Vspeed = V6 - 1200
        Vspeed *= -1
        Vspeed /= 3 
        
        print("M1 BACKWARD! "+str(V6)+str(int(Vspeed)))
        myMotor1.setSpeed(int(Vspeed))
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
    
    inputVal7 = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)
    V7 = float(inputVal7)
    print("V7="+str(V7))
    if 1200 < V7 < 4095:
        Vspeed = V7 - 1200
        Vspeed /= 3 

        print("M2 Forward! "+str(V7))
        myMotor2.setSpeed(int(Vspeed))
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
    if 0 < V7 < 1200:
        Vspeed = V7 - 1200
        Vspeed *= -1
        Vspeed /= 3 

        print("M2 BACKWARD! "+str(V7))
        myMotor2.setSpeed(int(Vspeed))
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        
    time.sleep(0.5)
    myMotor1.setSpeed(0)
    myMotor2.setSpeed(0)
        
 
    #print("Release")
    #myMotor1.run(Adafruit_MotorHAT.RELEASE)
    #myMotor2.run(Adafruit_MotorHAT.RELEASE)
    
    #time.sleep(1.0)
