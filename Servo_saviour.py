# MANSEDS Lunar Rover - Servo Saviour
# Author: Ethan Ramsay

import logging
import Adafruit_PCA9685


# Retrieve last servo channel and current pulse length from servo log
with open(servo.log) as log:
    penult = None
    last = None
    for last in (line for line in log if line.rstrip('\n')):
        penult = last
        last = line
channel = int(penult.split(":0")[1])
pl_init = int(last.split(": ")[1])


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Servo saviour main
for pl in range(0, pl_init, -32):
    pwm.set_pwm(channel, 0, pl)
