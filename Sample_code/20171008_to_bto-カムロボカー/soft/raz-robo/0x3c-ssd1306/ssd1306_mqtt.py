# -*- coding: utf-8 -*-

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
 
#import Image
#import ImageDraw
#import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import smbus
import time
import paho.mqtt.client as mqtt
import atexit
import json

gyou1 = 'gyou ssd1306 '

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    global gyou1 
    font = ImageFont.truetype('/home/pi/font/misakifont/misaki_gothic.ttf', 16, encoding='unic')
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print(str(msg.payload))
    r = (str(msg.payload))
    print(r)
   
    r0=r.replace("b'","")
    r0=r0.replace("'","")
    print(r0)
    gyou1 = r0
  # Main program block
  # Write two lines of text.
    x=0
    y=0
    for str1 in [ u'',gyou1 ]:
                draw.text((x,y), str1, font=font, fill=255)
                y+=16

    disp.image(image)
    disp.display()

#    lcd_string(gyou1,LCD_LINE_1)    
    
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)




# Raspberry Pi pin configuration
RST = 24

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()
 
# Clear display.
disp.clear()
disp.display()
 
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Misaki Font, awesome 8x8 pixel Japanese font, can be downloaded from the following URL.
# $ wget http://www.geocities.jp/littlimi/arc/misaki/misaki_ttf_2015-04-10.zip
#font = ImageFont.truetype('/home/pi/font/misakifont/misaki_gothic.ttf', 8, encoding='unic')
font = ImageFont.truetype('/home/pi/font/misakifont/misaki_gothic.ttf', 16, encoding='unic')

# Un-comment out the following line if you want to use the default font instead of Misaki Font
# font = ImageFont.load_default()
gyou1 = 'gyou ssd1306 '
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("Out-ssd1306",0)

mqttc.loop_start()






# Write two lines of text.
x=0
y=0
#for str in [ u'最近の研究から、地球上のカミナ', u'リ雲でも電子が高いエネルギーに', u'まで「加速」されている証拠が見', u'つかってきました。加速された電', u'子が大気分子と衝突することで生', u'じるガンマ線がカミナリ雲からビ', u'ーム状に放出されていることがわ', u'かったのです！  →   thdr.info' ]:
#	draw.text((x,y), str, font=font, fill=255)
#	y+=8

#for str in [ u'ＳＳＤ１３０６試験表示', u'ＤＯＴ：１６', u'128*64ピクセル', u'８文字*４行', u'５行目', u'６行目' ]:
#	draw.text((x,y), str, font=font, fill=255)
#	y+=16
for str1 in [ u'',gyou1 ]:
	draw.text((x,y), str1, font=font, fill=255)
	y+=16

disp.image(image)
disp.display()

def main():
  # Main program block
        # Write two lines of text.
  x=0
  y=0
  while True:
    #for str in [ u'',gyou1 ]:
    #            draw.text((x,y), str, font=font, fill=255)
    #            y+=16

    #disp.image(image)
    #disp.display()


    time.sleep(3)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  #finally:
    #lcd_byte(0x01, LCD_CMD)


