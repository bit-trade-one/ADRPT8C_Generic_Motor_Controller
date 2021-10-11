# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685


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
#        0.5ms --1.45ms -- 2.4ms /20ms
#        0.025 --0.0725 -- 0.12  /1
#        102   ---297  ----492  195/390/4096
#        -90       0       +90    390 0.46
#   input * 390
#   input + 297
#        0.5ms --1.45ms -- 2.4ms /20ms
#        0.025 --0.0725 -- 0.12  /1
#        102   ---185  ----258  83/156/4096
#        -90       0       +90    390 0.46
#   input * 156
#   input + 185

#v = 0

v1 = float(sys.argv[1])
#v1 = 0.5
#v1 = -0.5
v1 *= 156
v1 += 162
#v1 =  2048

v2 = float(sys.argv[1])
#v2 = 0.5
#v12= -0.5

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
#pwm.set_pwm(1, 4096-v, v)
#pwm.set_pwm(1, 4096-v, v)
#set_servo_pulse(0, 600)
#pwm.set_pwm(1, 1, servo_max)
#time.sleep(1)
#pwm.set_pwm(0, 4096-v, v)
#pwm.set_pwm(0, 1, servo_max)
#set_servo_pulse(0, 600)
#pwm.set_pwm(1, 1, servo_min)
time.sleep(1)

