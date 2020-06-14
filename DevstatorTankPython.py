#!/usr/bin/python
from evdev import InputDevice , categorize, ecodes
from select import select
import time
import sys

# keyboard events only
dev = InputDevice('/dev/input/event3') 
print(dev)

import Robot
#from HCSR04Sensor import distance
#from neopixel_rpi_python import *

from Raspi_PWM_Servo_Driver import PWM

# ===========================================================================
# Servo Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x6F)
servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
pwm.setPWMFreq(60)   # Set frequency to 60 Hz

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print ("%d us per period" % pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print ("%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

# Set the trim offset for each motor (left and right).    
LEFT_TRIM   = 0
RIGHT_TRIM  = 0

# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - left_id: The ID of the left motor, default is 1.
#  - right_id: The ID of the right motor, default is 2.
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)    

def check_distance():
# check distance b4 moving. NOT USED
    curDis = distance()
    print('Current distance in CM: ', curDis)
    if distance() < 15:
        print('Too Close!, Reversing ')
        robot.backward(100, 0.5)
        robot.stop()
    if distance() < 15:
        print('Too Close!, Reversing ')
        robot.backward(100, 0.5)
        robot.stop()
    if distance() < 15:
        print('Too Close!, Reversing ')
        robot.backward(100, 0.5)
        robot.stop()
    else:
        print('WAY Too Close!, Stopping ')
        robot.stop()
        
# Use the arrow keys to control the robot
def key_input(event):
    #print ('Key:', event.value, event.code)
    #sleep_time = 0.030
#   UP arrow key    
    if (event.code == 103 and event.value == 0):
        #check_distance()
        print ("Forward")
        robot.forward(150)
        sleep_time = 0.030
    elif (event.code == 108 and event.value == 0):
        #check_distance()
        print  ("Back")
        robot.backward(150)
        sleep_time = 0.030
    elif (event.code == 106 and event.value == 0):
        #check_distance()
        print ("right")
        robot.right(100, 0.15)
        sleep_time = 0.030
    elif (event.code == 105  and event.value == 0):
        #check_distance()
        print ("left")
        robot.left(100, 0.15)
        sleep_time = 0.030
#   press S key to control servo        
    elif (event.code == 115  and event.value == 0):
  # Change speed of continuous servo on channel O
        pwm.setPWM(0, 0, servoMin)
        time.sleep(0.5)
        pwm.setPWM(0, 0, servoMax)
        time.sleep(0.5)        
# enter = stop        
    elif event.code == 28:
        print ("stop")
        robot.stop()         
    else:
        pass

try:
        for event in dev.read_loop():
# start LED's blinking. sleep for 5 ms after each cycle           
            #rainbow_cycle(0.005)
            #check_distance()
            key_input(event)
            
except KeyboardInterrupt:
    print ('Interrupted')
    sys.exit(0)
