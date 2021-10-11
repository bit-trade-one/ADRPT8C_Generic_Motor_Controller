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
        V0 -=2000.0
        V0 /= 4096.0 #seikika
        print(" ="+str(V0),end='')
        #msg = "%s" % (inputVal0)
        (rc, mid) = mqttc.publish("In-ch0",str(V0), qos=2)
        #(rc, mid) = mqttc.publish("In-ch0", msg, qos=2)
        #f = open("/tmp/mcp3208-ch0.txt","w")
        #f.write(msg)
        #f.close()
        
        #sleep(1.0)
        
        
        inputVal2 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        V2 = float(inputVal2)
        #print("    ch2="+str(V2),end='')
        V2 -=2000.0
        V2 /= 4096.0 #seikika
        print(" ="+str(V2))
        (rc, mid) = mqttc.publish("In-ch2",str(V2), qos=2)
        
        #print(" ch2="+str(inputVal2)),
        #msg = "%s" % (inputVal2)
        #f = open("/tmp/mcp3208-ch2.txt","w")
        #f.write(msg)
        #f.close()
        
        
        #print("tuple")
        #(rc, mid) = mqttc.publish("In-ch0", 0.5, qos=2)
        #(rc, mid) = mqttc.publish("In-ch0", 0, qos=2)
        #(rc, mid) = mqttc.publish("In-ch0", -0.5, qos=2)
        
        
        sleep(0.1)
except KeyboardInterrupt:
    pass
#f.close()
GPIO.cleanup()
