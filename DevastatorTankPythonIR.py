#!/usr/bin/env python3
# John Franklyn 07/07/2020
''' Based on the Geekworm motor HAT and the RaspiMotor code
# Based on irw.c, https://github.com/aldebaran/lirc/blob/master/tools/irw.c
# Read IR sensor, lirc output, in order to sense key presses on an IR remote.
# Based on LED codes from instructibles

'''
import socket
import time
import sys
import Robot
#from HCSR04Sensor import distance
import RPi.GPIO as GPIO
from led import Led
from led_effects import LedEffects
from Raspi_PWM_Servo_Driver import PWM

def start(effects):
    effects.blink_in_series_non_stop()

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

''' ===========================================================================
# Servo Code to control a digital servo using GPIO
 ===========================================================================
''' 
fPWM = 50
#pwm = PWM(0x6F) # (standard) adapt to your module
channel = 12 # adapt to your wiring
a = 8.5 # adapt to your servo
b = 2  # adapt to your servo

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT) # red
GPIO.setup(18, GPIO.OUT) # yellow
GPIO.setup(22, GPIO.OUT) # green
GPIO.setup(12, GPIO.OUT) # servo motor

global pwm
pwm=GPIO.PWM(channel, 50)
pwm.start(0)

def setDirection(direction):
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty) # left -90 deg position    
    print ("direction =", direction, "-> duty =", duty)
    time.sleep(1) # allow to settle

# initialize list object for LED's
leds = list()
a_led_effects = LedEffects(leds)

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

try:
# Initialize objects and variables
    init()
               
    while True:
        '''   get the remote key codes and match those to tank movements
        00 = key down, 01 = key up '''

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
        elif (str_keyname == 'KEY_5' and str_updown == '00'):
            print ("Servo Control")
            for direction in range(0, 181, 10):
                setDirection(direction)
            direction = 0    
            setDirection(0)  
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
            led_16 = Led(16)
            leds.append(led_16)
            led_18 = Led(18)
            leds.append(led_18)
            led_22 = Led(22)
            leds.append(led_22)

            start(a_led_effects)            

        else:
            pass        

except SystemExit:
    print ('Quiting program')
finally:
    for led in leds:
        led.clean_up()    
