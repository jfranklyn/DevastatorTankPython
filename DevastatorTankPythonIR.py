#!/usr/bin/env python3
# John Franklyn 07/07/2020
''' Based on the Geekworm motor HAT and the RaspiMotor code
# Based on irw.c, https://github.com/aldebaran/lirc/blob/master/tools/irw.c
# Read IR sensor, lirc output, in order to sense key presses on an IR remote.
from Raspi_PWM_Servo_Driver import PWM
'''
import socket
import time
import sys
import Robot
#from HCSR04Sensor import distance
import RPi.GPIO as GPIO

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print ("%d us per period" % pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print ("%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

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

'''Add all initialization code here. This gets called once on startup
   Create a socket for the infrared data stream of key codes
'''
def init():
    SOCKPATH = "/var/run/lirc/lircd"
    global sock
    sock = None
    
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print ('starting up on %s' % SOCKPATH)
    sock.connect(SOCKPATH)

# Set the trim offset for each motor (left and right).    
LEFT_TRIM   = 0
RIGHT_TRIM  = 0

''' Create an instance of the robot with the specified trim values.
 Not shown are other optional parameters:
  addr: The I2C address of the motor HAT, default is 0x60.
   left_id: The ID of the left motor, default is 1.
   right_id: The ID of the right motor, default is 2.
    global robot
'''
global robot
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# ===========================================================================
# Servo Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
##pwm = PWM(0x6F)
##servoMin = 150  # Min pulse length out of 4096
##servoMax = 600  # Max pulse length out of 4096
##pwm.setPWMFreq(60)   # Set frequency to 60 Hz

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

def next_key():
    '''Get the next key pressed. Return keyname,  key up/down status.
    '''
    while True:
        data = sock.recv(128)

        data = data.strip()
        #print("Data after strip: " , data)
        if data:
            break

    words = data.split()
    
    return words[2], words[1]

# flash LED lights
def flash_leds():
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(18,GPIO.HIGH)  
    GPIO.output(22,GPIO.HIGH)
    time.sleep(5)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)  
    GPIO.output(22,GPIO.LOW)
    time.sleep(5)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(18,GPIO.HIGH)  
    GPIO.output(22,GPIO.HIGH)
    time.sleep(5)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)  
    GPIO.output(22,GPIO.LOW)
    

try:
# Initialize objects and variables
    init()
               
    while True:
#   get the remote key codes and match those to tank movements
#   00 = key down, 01 = key up
        b_keyname, b_updown = next_key()
        str_keyname = b_keyname.decode()
        str_updown = b_updown.decode()
        print('strings:' , str_keyname, str_updown)
        if (str_keyname == 'KEY_UP' and str_updown == '00'):
            #check_distance()
            print ("Forward")
            robot.forward(150)
            sleep_time = 0.030
        elif (str_keyname == 'KEY_DOWN' and str_updown == '00'):
            #check_distance()
            print  ("Back")
            robot.backward(150)
            sleep_time = 0.030
        elif (str_keyname == 'KEY_RIGHT' and str_updown == '00'):
            #check_distance()
            print ("right")
            robot.right(100, 0.15)
            sleep_time = 0.030
        elif (str_keyname == 'KEY_LEFT' and str_updown == '00'):
            #check_distance()
            print ("left")
            robot.left(100, 0.15)
            sleep_time = 0.030
    #   press 5 key to control servo        
        #elif (str_keyname == 'KEY_5' and str_updown == '00'):
      # Change speed of continuous servo on channel O
##            pwm.setPWM(0, 0, servoMin)
##            time.sleep(0.5)
##            pwm.setPWM(0, 0, servoMax)
##            time.sleep(0.5)        
    # enter = stop        
        elif (str_keyname == 'KEY_0' and str_updown == '00'):
            print ("stop")
            robot.stop()
    # controlling the lights        
        elif (str_keyname == 'KEY_1' and str_updown == '00'):
            print ("red light")
            GPIO.output(16,GPIO.HIGH)
            time.sleep(1)
            #print ("LED off")
            GPIO.output(16,GPIO.LOW)
        elif (str_keyname == 'KEY_2' and str_updown == '00'):
            print ("green light")
            GPIO.output(18,GPIO.HIGH)
            time.sleep(1)
            #print ("LED off")
            GPIO.output(18,GPIO.LOW)
        elif (str_keyname == 'KEY_3' and str_updown == '00'):
            print ("yellow light")
            GPIO.output(22,GPIO.HIGH)
            time.sleep(1)
            #print ("LED off")
            GPIO.output(22,GPIO.LOW)
        elif (str_keyname == 'KEY_4' and str_updown == '00'):
            print ("flash lights")
            flash_leds()
        else:
            pass        

except KeyboardInterrupt:
    print ('Interrupted')
    GPIO.cleanup()
    sys.exit(0)
