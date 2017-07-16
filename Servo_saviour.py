# MANSEDS Lunar Rover - Servo Saviour
# Author: Ethan Ramsay

import time
import logging
import Adafruit_PCA9685


# Retrieve last servo channel and current pulse length from servo log
with open("servo.log") as log:
    line = None
    triult = None
    penult = None
    last = None
    for last in (line for line in log if line.rstrip('\n')):
        triult = penult
        penult = last
        last = line
print(triult.split(": ")[1])
print(penult.split(": ")[1])
print(last)
channel = int(triult.split(": ")[1])
pl_init = int(penult.split(": ")[1])
print(channel)
print(pl_init)


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Servo saviour main
for val in range(0, pl_init, 32):
    pl = pl_init - val
    pwm.set_pwm(channel, 0, pl)
    time.sleep(0.1)
    print(pl)
