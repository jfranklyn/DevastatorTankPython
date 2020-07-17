#!/usr/bin/python

import sys
from led import Led
from led_effects import LedEffects

def start(effects):
    effects.blink_in_series_non_stop()
    
def main():
    leds = list()
    a_led_effects = LedEffects(leds)
    try:
        led_11 = Led(16)
        leds.append(led_11)
        led_12 = Led(18)
        leds.append(led_12)
        led_15 = Led(22)
        leds.append(led_15)

        start(a_led_effects)
    except SystemExit:
        print ('Quiting program')
    finally:
        for led in leds:
            led.clean_up()
        
if __name__ == "__main__":
    main()
