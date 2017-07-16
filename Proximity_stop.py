# MANSEDS Lunar Rover -- Proximity Sensor Auto-stop & Warning
# Author: Ethan Ramsay


# Import dependencies
import RPi.GPIO as GPIO
import logging
from Motor_brake import motor_brake


# Logging config
logging.basicConfig(filename='proximity.log', level=logging.DEBUG)


# System variables
near_pins = [0, 0, 0]
far_pins = [0, 0, 0]
motor_hilo_pins= [[0, 0], [0, 0], [0, 0], [0, 0]]


# Set index from last line of proximity log
with open("proximity.log") as log:
    last = None
    for last in (line for line in log if line.rstrip('\n')):
        last = line
index = int(last.split("|")[0]) + 1


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(near_pins, GPIO.IN)
GPIO.setup(far_pins, GPIO.IN)
logging.debug("%s| Proximity sensors on GPIO pins %s & %s set to GPIO input", + \
                        index, near_pins, far_pins)
index += 1


# Interrupt functions
def stop():
    motor_brake(motor_hilo_pins)
    logging.debug("%s| 5cm proximity sensor pin %s triggered, activate motor break", + \
                            index, pin)
    index += 1


def warn():
    logging.debug("%s| 10cm proximity sensor pin %s triggered", index, pin)
    index += 1


# Main
if __name__ == "__main__":
    GPIO.add_event_detect(near_pins, GPIO.FALLING, callback=stop)
    GPIO.add_event_detect(far_pins, GPIO.FALLING, callback=warn)
