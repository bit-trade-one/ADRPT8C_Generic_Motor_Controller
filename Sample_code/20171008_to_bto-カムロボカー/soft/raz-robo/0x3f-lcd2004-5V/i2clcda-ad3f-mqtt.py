# _____ _____ _____ __ __ _____ _____ 
#|     |   __|     |  |  |     |     |
#|  |  |__   |  |  |_   _|  |  |  |  |
#|_____|_____|_____| |_| |_____|_____|
#
# Project Tutorial Url:http://osoyoo.com/?p=1031
#  
import smbus
import time
import paho.mqtt.client as mqtt
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit

import json

gyou1 = 'gyou1  '
gyou2 = 'gyou2  '
gyou3 = 'gyou3  '
gyou4 = 'gyou4  '

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    global gyou1 
    global gyou2
    global gyou3
    global gyou4  
    
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #print(str(msg.payload))
    r = (str(msg.payload))
    print(r)
    #r4 = 'init  '
    #print(gyou4)
    gyou4 = gyou3
    gyou3 = gyou2
    gyou2 = gyou1


    

    #print(gyou4)
    
    r0=r.replace("b'","")
    r0=r0.replace("'","")
    print(r0)
    gyou1 = r0
    
    lcd_string(gyou1,LCD_LINE_1)    
    lcd_string(gyou2,LCD_LINE_2)    
    lcd_string(gyou3,LCD_LINE_3)    
    lcd_string(gyou4,LCD_LINE_4)    
    
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)



# Define some device parameters
#I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x3f
I2C_ADDR  = 0x3f # I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 20   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

gyou1 = 'gyou1      '
gyou2 = 'gyou2      '
gyou3 = 'gyou3      '
gyou4 = 'gyou4      '

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("Out-lcd2004",0)

mqttc.loop_start()



def main():
  # Main program block

  # Initialise display
  lcd_init()
    # Send some test
  lcd_string(gyou1,LCD_LINE_1)
  lcd_string(gyou2,LCD_LINE_2)

    #time.sleep(3)
  
    # Send some more text
  lcd_string(gyou3,LCD_LINE_3)
  lcd_string(gyou4,LCD_LINE_4)

  while True:
    
    # Send some test
    #lcd_string(gyou1,LCD_LINE_1)
    #lcd_string(gyou2,LCD_LINE_2)

    #time.sleep(3)
  
    # Send some more text
    #lcd_string(gyou3,LCD_LINE_3)
    #lcd_string(gyou4,LCD_LINE_4)

    time.sleep(3)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)

