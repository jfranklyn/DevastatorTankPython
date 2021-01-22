# DFRobot Devastator Tank Python Code
Raspberry Pi 4 B Python Code
Python version 3.7.3
DFRobot Deastator tank kit used for the robot
Geekworm Stepper motor HAT controlling all 4 motors
Raspi_MotorHAT code from Geekworm
Motors 1,2 used to control tank motors
Motors 3,4 used to control NERF canon mounted to the tank. Any motorized NERF canon could be used. I cut a lot of the plastic out of the NERF gun to make it smaller. I added a DC motor to control the plunger that feed the bullets into the gun.
Infrared code from lirc.com. This is a simplified implementation with the minimum of configuration files.
https://stackoverflow.com/questions/57437261/setup-ir-remote-control-using-lirc-for-the-raspberry-pi-rpi

Read IR sensor, lirc output, in order to sense key presses on an IR remote.
Not using the LED or servo code but I added it for testing:
Based on LED codes from instructibles
Added code to control digital servos using GPIO

The biggest problem was getting the signal to the sensors. The tank kit is metal, so that blocks a lot of signal.
The bluetooth receiver is on the RaspberryPi, which in under the motor HAT.
The RaspberryPi IR receiver is also under the motor HAT. Luckily I found the Geekworm HAT that had an IR receiver.


