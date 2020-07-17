#!/usr/bin/python

import RPi.GPIO
import time

class Led(object):
    '''
    Represents a physical LED. It uses the RPi GPIO naming scheme and NOT Broadcomm's
    '''
    def __init__(self, pin_number):
        '''
        Set up the hardware connection
        Params: pin_number of type int - Follow RPi GPIO naming scheme
        '''
        self.pin_number = pin_number
        self.__setup_gpio__()

    def __setup_gpio__(self):
        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        RPi.GPIO.setup(self.pin_number, RPi.GPIO.OUT)

    def clean_up(self):
        '''
        Reset the GPIO header to its initial state.
        '''
        RPi.GPIO.cleanup(self.pin_number)
   
    def on_light(self):
        '''
        Switch on the LED
        '''
        RPi.GPIO.output(self.pin_number, True)

    def off_light(self):
        '''
        Switch off the LED
        '''
        RPi.GPIO.output(self.pin_number, False)

    def blink(self, drift_time=0.2):
        self.on_light()
        time.sleep(float(drift_time))
        self.off_light()
        time.sleep(float(drift_time))

    def blinkn(self, number_times):
        '''
        Blink for any number of times
        Param: number_times of type int
        '''
        for i in range(0, int(number_times)):
            self.blink()

    def blink_non_stop(self):
        while True:
            self.blink()
