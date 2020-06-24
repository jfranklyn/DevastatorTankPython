#
# Boot script, called by cron using @reboot
#
# John Franklyn 06/24/2020
#

import time
import subprocess

# functions
def speak(phrase):
    p1 = subprocess.Popen(['echo', phrase], stdout=subprocess.PIPE)
    subprocess.Popen(['festival', '--tts'], stdin=p1.stdout).wait()

# main
print("starting boot script")

# monitor shutdown button 
print("press the black button to shut down")
#subprocess.Popen(['sudo', 'python', '/home/jfranklyn/PythonCode/DevastatorTankPython/boot/shutdownbutton.py'])

# start the Bluetooth server for robot functions
print("starting the bluetooth server")
logfile = open('/home/jfranklyn/PythonCode/DevastatorTankPython/log/roboserver-bt.log', 'w')
errfile = open('/home/jfranklyn/PythonCode/DevastatorTankPython/log/roboserver-bt.err', 'w')
subprocess.Popen(['sudo', 'python', '/home/jfranklyn/PythonCode/DevastatorTankPython/DevastatorTankserver-bt.py'], stdout=logfile, stderr=errfile)

# end
