# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

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

#try:
    #while True:
if __name__ == '__main__':
        inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal0),
        msg = "%s" % (inputVal0)
        f = open("/tmp/mcp3208-ch0.txt","w")
        f.write(msg)
        f.close()
        inputVal1 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal1),
        msg = "%s" % (inputVal1)
        f = open("/tmp/mcp3208-ch1.txt","w")
        f.write(msg)
        f.close()        
        inputVal2 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal2),
        msg = "%s" % (inputVal2)
        f = open("/tmp/mcp3208-ch2.txt","w")
        f.write(msg)
        f.close()
        inputVal3 = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal3),
        msg = "%s" % (inputVal3)
        f = open("/tmp/mcp3208-ch3.txt","w")
        f.write(msg)
        f.close()        
        inputVal4 = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal4),
        msg = "%s" % (inputVal4)
        f = open("/tmp/mcp3208-ch4.txt","w")
        f.write(msg)
        f.close()        
        inputVal5 = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal5),
        msg = "%s" % (inputVal5)
        f = open("/tmp/mcp3208-ch5.txt","w")
        f.write(msg)
        f.close()        
        inputVal6 = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal6),
        msg = "%s" % (inputVal6)
        f = open("/tmp/mcp3208-ch6.txt","w")
        f.write(msg)
        f.close()        
        inputVal7 = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print(inputVal7)
        msg = "%s" % (inputVal7)
        f = open("/tmp/mcp3208-ch7.txt","w")
        f.write(msg)
        f.close()        
        #sleep(0.2)
        #GPIO.cleanup()
        
#except KeyboardInterrupt:
    #pass

#GPIO.cleanup()
