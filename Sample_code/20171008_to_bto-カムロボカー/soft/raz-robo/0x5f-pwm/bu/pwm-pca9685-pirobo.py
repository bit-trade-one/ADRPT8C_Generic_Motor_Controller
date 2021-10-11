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


from __future__ import division
import time
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685
import paho.mqtt.client as mqtt

host = '127.0.0.1'
port = 1883
keepalive = 60
topic = 'mqtt/test'


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

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

#v1 = float(sys.argv[1])
v1 = 0.5
#v1 = -0.5
v1 *= 156
v1 += 162
#v1 =  2048

#v2 = float(sys.argv[1])
v2 = 0.5
#v2= -0.5

v2 *= -156
v2 += 162

v = int(v1)
#v=185
print('Moving servo on channel 0, press Ctrl-C to quit...')
print('v=')
print(v)
#while True:
    # Move servo on channel O between extremes.
#v = v + 400
if v > 4096:
    v = 0
pwm.set_pwm(0, 4096-v, v)

v = int(v2)
#v=185
print('Moving servo on channel 0, press Ctrl-C to quit...')
print('v=')
print(v)
#while True:
    # Move servo on channel O between extremes.
#v = v + 400
if v > 4096:
    v = 0
pwm.set_pwm(1, 4096-v, v)

time.sleep(1)
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

