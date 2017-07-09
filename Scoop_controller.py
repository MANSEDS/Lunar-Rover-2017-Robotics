# MANSEDS Lunar Rover -- Scoop Controller
# Author: Ethan Ramsay

# Abbreviations:
# dc = duty cycle
# pl = pulse length
# lin_act | lin = linear actuator
# e = extension
# a = angle
# pwm = pulse width modulation pin no.
# chan = pulse width modulation channel


# Import dependencies
import argparse
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import logging


# Logging config
logging.basicConfig(filename='scoop.log', level=logging.DEBUG)

# System variables
lin_act = 0
servos = []
lin_pwm = 0
servo_pwm = [0, 0]
lin_dc_range = [0, 100]
servo_dc_range = [[0, 100], [0, 100]]
lin_chan = 12
servo_chan = [13, 14]
lin_pl_range = [0, 4095]
servo_pl_range = [0, 4095]


# GPIO setup function
def GPIO_set(dc):
    for i in range(0,2,1):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pwm[i], GPIO.OUT)
        servos.append(GPIO.PWM(servo_pwm[i], 60))
    GPIO.setup(lin_pwm, GPIO.OUT)
    lin_act = GPIO.PWM(lin_pwm, 60)


def GPIO_clear(lin_act):
    for servo in servos:
        servo.stop()
    lin_act.stop()
    GPIO.cleanup()


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Signal functions
def calc_dc(dc_min, dc_max, magnitude, maximum):
    dc_range = dc_max - dc_min
    inter = dc_range * magnitude / maximum
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired extension: %s", dc)
    return dc


def calc_pl(pl_min, pl_max, magnitude, maximum):
    pl_range = pl_max - pl_min
    inter = pl_range * magnitude / maximum
    pl = pl_min + inter
    logging.debug("Calculated required pulse length for desired extension: %s", pl)
    return pl


# Command functions
def scoop():
    pass


def adjust_pos(axis, direction):
    if axis == "hor":
        if direction == "forward":
            pass
        elif direction == "backwards":
            pass
    elif axis == "ver":
        if direction == "up":
            pass
        elif direction == "down":
            pass


if __name__ = "__main__":
    # Arguments
    parser = argparse.ArgumentParser()

    # Command arguments
    g = parser.add_mututally_exclusive_group(required=True)
    gh = g.add_mututally_exclusive_group()
    gv = g.add_mututally_exclusive_group()
    g.add_argument("-s", "--scoop", help="Scoop up")
    g.add_argument("", "", help="")
    gh.add_argument("-u", "--up", help="Vertically up")
    g.add_argument("", "", help="")
    gv.add_argument("-f", "--forward")
    g.add_argument("", "", help="")

    # Optional arguments

    # Parse arguments
    args = parser.parse_args()

    # Such empties
