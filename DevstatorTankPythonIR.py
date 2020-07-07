#!/usr/bin/env python3
# John Franklyn 07/07/2020
# Based on the Geekworm motor HAT and the RaspiMotor code
# Read lirc output, in order to sense key presses on an IR remote.
# Based on irw.c, https://github.com/aldebaran/lirc/blob/master/tools/irw.c

import socket
SOCKPATH = "/var/run/lirc/lircd"
sock = None

#from evdev import InputDevice , categorize, ecodes
#from select import select
import time
import sys
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

#   Create a socket for the infrared data stream of key codes
def init_irw():
    global sock
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print ('starting up on %s' % SOCKPATH)
    sock.connect(SOCKPATH)

def next_key():
    '''Get the next key pressed. Return keyname, updown.
    '''
    while True:
        data = sock.recv(128)
        # print("Data: " + data)
        data = data.strip()
        if data:
            break

    words = data.split()
    return words[2], words[1]

try:

# start LED's blinking. sleep for 5 ms after each cycle           
    #rainbow_cycle(0.005)
    #check_distance()
    init_irw()
               
    while True:
#   get the remote key codes and match those to tank movements
#   00 = key down, 01 = key up
        keyname, updown = next_key()
        print('%s (%s)' % (keyname, updown))
        if (keyname == 'KEY_UP' and updown == '00'):
            #check_distance()
            print ("Forward")
            robot.forward(150)
            sleep_time = 0.030
        elif (keyname == 'KEY_DOWN' and updown == '00'):
            #check_distance()
            print  ("Back")
            robot.backward(150)
            sleep_time = 0.030
        elif (keyname == 'KEY_RIGHT' and updown == '00'):
            #check_distance()
            print ("right")
            robot.right(100, 0.15)
            sleep_time = 0.030
        elif (keyname == 'KEY_LEFT' and updown == '00'):
            #check_distance()
            print ("left")
            robot.left(100, 0.15)
            sleep_time = 0.030
    #   press 5 key to control servo        
        elif (keyname == 'KEY_5' and updown == '00'):
      # Change speed of continuous servo on channel O
            pwm.setPWM(0, 0, servoMin)
            time.sleep(0.5)
            pwm.setPWM(0, 0, servoMax)
            time.sleep(0.5)        
    # enter = stop        
        elif (keyname == 'KEY_0' and updown == '00'):
            print ("stop")
            robot.stop()         
        else:
            pass        

except KeyboardInterrupt:
    print ('Interrupted')
    sys.exit(0)
