#!/usr/bin/env python3
# John Franklyn 01/22/2021
'''
This is a copy of the Robot class used to control a NERF canon
Any motorized Nerf gun will work for this. The motors are 6V and 1A. I'm
using the Geekworm motor HAT to control all the motors
    StartCanon turns on/off the DC motor for the canon
    FireCanon turns on the DC motor to enable the plunger that fires the canon
This uses the Geekworm Stepper Motor HAT python code. In this case the motors
only have to turn on/off at full speed, so the coding is minimal
The motor numbering is hard-coded based on the motor HAT wiring
'''
import time
import atexit

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

class StartCanon(object):
    def __init__(self, addr=0x6f, left_id=3, stop_at_exit=True):
        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - left_id: The ID of the left motor, hard-coded to motor 3.
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and left, right motor.
        self._mh = Raspi_MotorHAT(addr)
        self._left = self._mh.getMotor(left_id)
        # Start with motors turned off.
        self._left.run(Raspi_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    # These motors will always run at full speed
    def _left_speed(self, speed=254):
        """Set the speed of the left motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += 0 # no tirm
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._left.setSpeed(speed)

    def stop(self):
        """Stop all movement."""
        self._left.run(Raspi_MotorHAT.RELEASE)

    def forward(self, speed=254, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._left.run(Raspi_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed=254, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._left_speed(speed)
        self._left.run(Raspi_MotorHAT.BACKWARD)        
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

class FireCanon(object):
    def __init__(self, addr=0x6f, right_id=4, stop_at_exit=True):
        """Create an instance of the canon.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - right_id: The ID of the right motor, hard-coded to motor 4.
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        This controls the plunger motor forward/backward motion
        that pushes the darts into the canon bore
        """
        # Initialize motor HAT and left, right motor.
        self._mh = Raspi_MotorHAT(addr)
        self._right = self._mh.getMotor(right_id)
        # Start with motors turned off.
        self._right.run(Raspi_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    # These motors will always run at full speed
    def _right_speed(self, speed=254):
        """Set the speed of the right motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += 0 # no trim for these motors
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._right.setSpeed(speed)

    def stop(self):
        """Stop all movement."""
        self._right.run(Raspi_MotorHAT.RELEASE)

    def forward(self, speed=254, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._right_speed(speed)
        self._right.run(Raspi_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed=254, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._right_speed(speed)
        self._right.run(Raspi_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()
   
