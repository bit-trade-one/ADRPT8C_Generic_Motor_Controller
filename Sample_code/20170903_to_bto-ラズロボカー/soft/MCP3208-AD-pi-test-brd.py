# -*- coding: utf-8 -*-
# 2017/7/15 jh1cdv
#
# Input:MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
# Output: -0.5 --- 0 --- +0.5
#        mqtt topic=/In-ch0,1
#


import RPi.GPIO as GPIO
from time import sleep

import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt

import json


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


try:
    while True:
     if __name__ == '__main__':
         
         
        # id parameter empty will generate a random id for you.
        #mqttc = mqtt.Client()
        #mqttc.on_message = on_message
        #mqttc.on_connect = on_connect
        #mqttc.on_publish = on_publish
        #mqttc.on_subscribe = on_subscribe
        # Uncomment to enable debug messages
        # mqttc.on_log = on_log
        #mqttc.connect("localhost", 1883, 60)

        #mqttc.loop_start()

        inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V0 = float(inputVal0)
        #print("ch0="+str(V0),end='')
        #V0 -=2000.0
        #V0 /= 4096.0 #seikika
        print("V0="+str(V0))
        #msg = "%s" % (inputVal0)
        (rc, mid) = mqttc.publish("In-ch0",str(V0), qos=2)
        #(rc, mid) = mqttc.publish("In-ch0", msg, qos=2)
        #f = open("/tmp/mcp3208-ch0.txt","w")
        #f.write(msg)
        #f.close()
        
        sleep(0.1)
        inputVal1 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V1 = float(inputVal1)
        print("V1="+str(V1))
        (rc, mid) = mqttc.publish("In-ch1",str(V1), qos=2)
        
        inputVal2 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V2 = float(inputVal2)
        #print("    ch2="+str(V2),end='')
        #V2 -=2000.0
        #V2 /= 4096.0 #seikika
        print("V2="+str(V2))
        (rc, mid) = mqttc.publish("In-ch2",str(V2), qos=2)
        
        #print(" ch2="+str(inputVal2)),
        #msg = "%s" % (inputVal2)
        #f = open("/tmp/mcp3208-ch2.txt","w")
        #f.write(msg)
        #f.close()
        inputVal3 = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V3 = float(inputVal3)
        print("V3="+str(V3))
        (rc, mid) = mqttc.publish("In-ch3",str(V3), qos=2)
        
        inputVal4 = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V4 = float(inputVal4)
        print("V4="+str(V4))
        (rc, mid) = mqttc.publish("In-ch4",str(V4), qos=2)
        
        inputVal5 = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V5 = float(inputVal5)
        print("V5="+str(V5))
        (rc, mid) = mqttc.publish("In-ch5",str(V5), qos=2)
        
        inputVal6 = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V6 = float(inputVal6)
        print("V6="+str(V6))
        (rc, mid) = mqttc.publish("In-ch6",str(V6), qos=2)
        
        inputVal7 = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V7 = float(inputVal7)
        print("V7="+str(V7))
        (rc, mid) = mqttc.publish("In-ch7",str(V7), qos=2)
        
        #tasks =  [{"ch0":V0,"ch1":V1}]
        tasks =  {"ch0":V0,"ch1":V1,"ch2":V2,"ch3":V3,"ch4":V4,"ch5":V5,"ch6":V6,"ch7":V7} 


        print(tasks )
        #(rc, mid) = mqttc.publish("In-ch0-7",payload=jsonify({'readings': tasks}) , qos=2)
        (rc, mid) = mqttc.publish("In-ch0-7",payload= json.dumps(tasks) , qos=2)
        
       
        #(rc, mid) = mqttc.publish("In-ch0", 0.5, qos=2)
        #(rc, mid) = mqttc.publish("In-ch0", 0, qos=2)
        #(rc, mid) = mqttc.publish("In-ch0", -0.5, qos=2)
        
        
        sleep(0.1)
except KeyboardInterrupt:
    pass
#f.close()
GPIO.cleanup()
