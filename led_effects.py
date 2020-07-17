#!/usr/bin/python

class LedEffects(object):
    def __init__(self, leds):
        self.leds = leds

    def blink_in_series(self):
        for led in self.leds:
            led.blink(0.1)

    def blink_in_seriesn(self, number):
        for i in range (0, number):
            self.blink_in_series()

    def blink_in_series_non_stop(self):
        while True:
            self.blink_in_series()
