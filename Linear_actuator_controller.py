# MANSEDS Lunar Rover -- Linear Actuator Controller
# Author: Ethan Ramsay

# Abbreviations:
# dc = duty cycle
# pl = pulse length
# lin_act = linear actuator
# e = extension
# pin = pulse width modulation pin no.


# Import dependencies
import argparse
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import logging


# Logging config
logging.basicConfig(filename='linact.log', level=logging.DEBUG)


# System variables
lin_act = 0


# GPIO setup function
def GPIO_set(pin, dc):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    lin_act = GPIO.PWM(pin, 50)
    lin_act.start(dc)


def GPIO_clear(lin_act):
    lin_act.stop()
    GPIO.cleanup()


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Signal functions
def calc_dc(dc_min, dc_max, extension):
    dc_range = dc_max - dc_min
    inter = dc_range * extension / 100
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired extension: %s", dc)
    return dc


def calc_pl(pl_min, pl_max, extension):
    pl_range = pl_max - pl_min
    inter = pl_range * angle / 100
    pl = pl_min + inter
    logging.debug("Calculated required pulse length for desired extension: %s", pl)
    return pl


if __name__ = "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("e", help="Extension %")

    # Arguments for direct GPIO control from Pi
    # parser.add_argument("dc_min", help="Minimum Duty Cycle")
    # parser.add_argument("dc_max", help="Maximum Duty Cycle")
    # parser.add_argument("pin", help="PWM Pin No. (BCM)")

    # Arguments for Adafruit PWM hat control
    parser.add_argument("pl_min", help="Minimum Pulse Length")
    parser.add_argument("pl_max", help="Maximum Pulse Length")
    parser.add_argument("channel", help="Channel No. (Adafruit PWM Hat)")

    # Parse arguments
    args = parser.parse_args()
    e = float(args.e)
    # dc_min = float(args.dc_min)
    # dc_max = float(args.dc_max)
    # pin = int(args.pin)
    pl_min = float(args.pl_min)
    pl_max = float(args.pl_max)
    channel = int(args.channel)


    # Calculate interpolated duty cycle
    # dc = calc_dc(dc_min, dc_max, e)


    # Calculate interpolated pulse length
    pl = calc_pl(pl_min, pl_max, a)

    # Actuate linear actuator
    # GPIO_set(pin, dc)
    # GPIO_clear()
    pwm.set_pwm(channel, 0, pl)


else:
    dc = calc_dc(0, 100, 75)
    pl = calc_pl(0, 4096, 75)
    print("Calculated duty cycle is: %s \n This should equal 75", dc)
    print("Calculated duty cycle is: %s \n This should equal 3072", pl)
