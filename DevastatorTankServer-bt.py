# 
# Bluetooth server for control of CamJam EduKit1 LEDs and EduKit3 Robot
#
# John Franklyn 06/24/2020
#
# includes parts of the GeekWorm robot.py
# includes parts of rfcomm-server.py by Albert Huang <albert@csail.mit.edu>
#

import RPi.GPIO as GPIO
import time
import subprocess
import json
from urllib import unquote_plus
from bluetooth import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#
# initialise GPIO pins for LEDs, buzzer and button
#

pinLEDs = {23:'red', 24:'yellow', 25:'green'}
for pin in pinLEDs:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

##pinButton = 26
##GPIO.setup(pinButton, GPIO.IN)
##
##pinBuzzer = 19
##GPIO.setup(pinBuzzer, GPIO.OUT)
##GPIO.output(pinBuzzer, GPIO.LOW)

#
# initialise I2C motor controller 
#

import Robot
#from HCSR04Sensor import distance
#from neopixel_rpi_python import *

from Raspi_PWM_Servo_Driver import PWM

# ===========================================================================
# Servo Code - not used
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
#
# initialise ultrasound module
#

# GPIO ultrasound module pins
pinTrigger = 17
pinEcho = 18
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)
GPIO.output(pinTrigger, GPIO.LOW)

#
# initialise line detector module
#

# GPIO line detector pin
pinLineFollower = 25
GPIO.setup(pinLineFollower, GPIO.IN)

#
# LED functions
#

def ledson():
    for pin in pinLEDs:
        GPIO.output(pin, GPIO.HIGH)

def ledsoff():
    for pin in pinLEDs:
        GPIO.output(pin, GPIO.LOW)

def flashleds(count):
    for i in range(count):
        ledsoff()
        time.sleep(0.2)
        ledson()
        time.sleep(0.2)
        ledsoff()

def ledcontrol(colour, state):
    for pin in pinLEDs:
        if pinLEDs[pin] == colour:
            if state == 'on':
                 GPIO.output(pin, GPIO.HIGH)
            elif state == 'off':
                 GPIO.output(pin, GPIO.LOW)

#
# buzzer functions
#

def buzzerbeep():
    GPIO.output(pinBuzzer, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(pinBuzzer, GPIO.LOW)
    time.sleep(0.1)

#
# ultrasound functions
#

def MeasureDistance():
    
    # send 10us pulse to Trigger
    GPIO.output(pinTrigger, GPIO.HIGH)
    time.sleep(0.000010)
    GPIO.output(pinTrigger, GPIO.LOW)
    
    # wait for start of Echo pin pulse
    StartTime = time.time()
    while GPIO.input(pinEcho) == GPIO.LOW:
        StartTime = time.time()
        
    # wait for end of Echo pin pulse
    StopTime = time.time()
    while GPIO.input(pinEcho) == GPIO.HIGH:
        StopTime = time.time()
        # long pulse indicates object is out of range (too near or too far)
        if StopTime - StartTime >= 0.030:
            StopTime = StartTime
            break
        
    # distance to object (in metres) is half of echo pulse length times speed of sound (m/s)
    distance = (StopTime - StartTime) * 343.26 / 2

    # warn if close to an obstacle
    if distance < 0.10 and distance != 0:
        ledcontrol('yellow', 'on')
        buzzerbeep()
    else:
        ledcontrol('yellow', 'off')

    return distance

#
# line detector functions
#

def BlackOrWhite():
    # sensor is high when reflection detected
    if GPIO.input(pinLineFollower) == GPIO.HIGH:
        return 'White'
    else:
        return 'Black'

#
# motor control functions
#

##def StopMotors():
##    pwmMotorAForwards.ChangeDutyCycle(Stop)
##    pwmMotorABackwards.ChangeDutyCycle(Stop)
##    pwmMotorBForwards.ChangeDutyCycle(Stop)
##    pwmMotorBBackwards.ChangeDutyCycle(Stop)
##
##def Forwards():
##    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
##    pwmMotorABackwards.ChangeDutyCycle(Stop)
##    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
##    pwmMotorBBackwards.ChangeDutyCycle(Stop)
##
##def Backwards():
##    pwmMotorAForwards.ChangeDutyCycle(Stop)
##    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
##    pwmMotorBForwards.ChangeDutyCycle(Stop)
##    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)
##
##def TurnLeft():
##    pwmMotorAForwards.ChangeDutyCycle(Stop)
##    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
##    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
##    pwmMotorBBackwards.ChangeDutyCycle(Stop)
##
##def TurnRight():
##    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
##    pwmMotorABackwards.ChangeDutyCycle(Stop)
##    pwmMotorBForwards.ChangeDutyCycle(Stop)
##    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)
##
### inputs are integers in range [-100, +100]
##def MotorSpeed(left, right):
##    if left > 0:
##        pwmMotorAForwards.ChangeDutyCycle(DutyCycleA * left / 100)
##        pwmMotorABackwards.ChangeDutyCycle(Stop)
##    else:
##        pwmMotorAForwards.ChangeDutyCycle(Stop)
##        pwmMotorABackwards.ChangeDutyCycle(DutyCycleA * abs(left) / 100)
##    if right > 0:
##        pwmMotorBForwards.ChangeDutyCycle(DutyCycleA * right / 100)
##        pwmMotorBBackwards.ChangeDutyCycle(Stop)
##    else:
##        pwmMotorBForwards.ChangeDutyCycle(Stop)
##        pwmMotorBBackwards.ChangeDutyCycle(DutyCycleA * abs(right) / 100)

#
# command functions
#

def root():
    return jsonstatus()

def beep():
    buzzerbeep()
    return jsonstatus()

def led():
    return jsonstatus()

def ledflash():
    flashleds(3)
    ledcontrol('green', 'on')
    return jsonstatus()
    
def ledstate(colour, state):
    ledcontrol(colour, state)
    return jsonstatus()

def robot():
    print ("stop")
    robot.stop()   
    ledcontrol('red', 'off')
    return jsonstatus()

def robotstop():
    print ("robotstop")
    robot.stop()   
    ledcontrol('red', 'off')
    return jsonstatus()

def robotforwards():
    print ("Forward")
    robot.forward(255)
    #sleep_time = 0.030
    flashleds(3)
    return jsonstatus()

def robotbackwards():
    print  ("Back")
    robot.backward(255)
    #sleep_time = 0.030
    flashleds(3)
    return jsonstatus()

def robotleft():
    robot.left(250, 0.25)
    #sleep_time = 0.030
    ledcontrol('green', 'on')
    return jsonstatus()

def robotright():
    robot.right(250, 0.25)
    #sleep_time = 0.030
    ledcontrol('red', 'on')
    return jsonstatus()

def robotmotors(left, right):
    # convert string arguments to integers
    left = int(left)
    right = int(right)
    # allowed range [-100, +100]
    if left > 100:
        left = 100
    elif left < -100:
        left = -100
    if right > 100:
        right = 100
    elif right < -100:
        right = -100
    MotorSpeed(left,right)
    ledcontrol('red', 'on')
    return jsonstatus()

def speak(phrase):
    phrase = unquote_plus(phrase)
    p1 = subprocess.Popen(['echo', phrase], stdout=subprocess.PIPE)
    subprocess.Popen(['festival', '--tts'], stdin=p1.stdout) # don't wait for process to end
    return jsonstatus()

def jsonstatus():
    status = {}
    for pin in pinLEDs:
        status[pinLEDs[pin]] = str(GPIO.input(pin))
    #status['distance'] = str(round(MeasureDistance() * 100, 1)) + ' cm'
    #status['surface'] = BlackOrWhite()
    # JSON encode and transmit response
    response = json.dumps(status)
    client_sock.send(response)
    return

#
# main loop
#

# add serial port service
subprocess.call(['sudo', 'sdptool', 'add', 'SP'])

# signal main loop start
flashleds(3)

try:
    while True:

        # start the Bluetooth service
        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)
        port = server_sock.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service( server_sock, "devtankserver-bt",
                           service_id = uuid,
                           service_classes = [uuid, SERIAL_PORT_CLASS],
                           profiles = [SERIAL_PORT_PROFILE] )
                           
        # signal server startup
        ledcontrol('yellow', 'on')

        # wait for connection
        client_sock, client_info = server_sock.accept()

        # signal successful connection
        ledcontrol('yellow', 'off')
        ledcontrol('green', 'on')

        # receiver loop
        try:
            partial = ''
            
            while True:

                # read from serial port receive buffer
                data = client_sock.recv(1024)
                if len(data) == 0:
                    break
                elif len(data) == 1024:
                    bufferfull = True
                else:
                    bufferfull = False

                # prepend any partial command from last time, then split commands
                commands = (partial + data).split('$$')
                number = len(commands)

                # full buffer means last command may not be complete, so hold it over
                if bufferfull:
                    partial = commands[number-1]
                    number -= 1
                else:
                    partial = ''

                # loop through commands
                for i in range(number):

                    # parse the command
                    command = commands[i]
                    parts = command.split('/')
                    count = len(parts)

                    if command == '':
                        continue
                    
                    elif command == '/':
                        root()
                        
                    elif command == '/beep':
                        beep()
                        
                    elif command == '/led':
                        led()
                        
                    elif command == '/led/flash':
                        ledflash()
                        
                    elif command[0:5] == '/led/' and count == 4:
                        colour = parts[2] # green, yellow, red
                        state = parts[3]  # on, off
                        ledstate(colour, state)

                    elif command == '/robot':
                        robot()

                    elif command == '/robot/stop':
                        robotstop()

                    elif command == '/robot/forwards':
                        robotforwards()

                    elif command == '/robot/backwards':
                        robotbackwards()

                    elif command == '/robot/left':
                        robotleft()

                    elif command == '/robot/right':
                        robotright()

                    elif command[0:14] == '/robot/motors/' and count == 5:
                        left = parts[3]  # integer 0-100
                        right = parts[4] # integer 0-100
                        robotmotors(left, right)

                    elif command[0:7] == '/speak/' and count == 3:
                        phrase = parts[2] # URI-encoded
                        speak(phrase)

                    else:
                        robotstop()
                        speak("error " + command)
                
        # receiver loop try
        except IOError:
            pass

        # connection lost
        client_sock.close()
        server_sock.close()

        # signal disconnect
        ledcontrol('green', 'off')

# main loop try
except KeyboardInterrupt:
    client_sock.close()
    server_sock.close()
    GPIO.cleanup()

