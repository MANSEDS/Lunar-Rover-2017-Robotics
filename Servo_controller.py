# MANSEDS Lunar Rover -- Servo Controller
# Author: Ethan Ramsay

# Abbreviations:
# dc = duty cycle
# pl = pulse length
# a = angle
# pin = pulse width modulation pin no.

# Import dependencies
import RPi.GPIO as GPIO
import logging
import Adafruit_PCA9685


# Logging config
logging.basicConfig(filename='servo.log', level=logging.DEBUG)

# System variables
pi = 3.14159
servo = 0

# GPIO setup function
def GPIO_set(pin, dc):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)
    servo.start(dc)


def GPIO_clear(servo):
    servo.stop()
    GPIO.cleanup()


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Funcs
def calc_dc(dc_min, dc_max, angle):
    dc_range = dc_max - dc_min
    inter = dc_range * angle / 180
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired angle: %s", dc)
    return dc


def calc_pl(pl_min, pl_max, angle):
    pl_range = pl_max - pl_min
    inter = pl_range * angle / 180
    pl = pl_min + inter
    logging.debug("Calculated required pulse length for desired angle: %s", pl)
    return pl


if __name__ == "__main__":

    import argparse

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("a", help="Angle (Degrees)")

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
    a = float(args.a)
    # dc_min = float(args.dc_min)
    # dc_max = float(args.dc_max)
    # pin = int(args.pin)
    pl_min = float(args.pl_min)
    pl_max = float(args.pl_max)
    channel = int(args.channel)
    logging.debug("Channel: %s", channel)


    # Calculate interpolated duty cycle
    # dc = calc_dc(dc_min, dc_max, a)


    # Calculate interpolated pulse length
    pl = calc_pl(pl_min, pl_max, a)
    pl = int(pl)

    # Actuate servo
    while True:
        # GPIO_set(pin, dc)
        # GPIO_clear()
        pwm.set_pwm(channel, 0, pl)

else:
    dc = calc_dc(dc_min, dc_max, a)
    pl = calc_pl(pl_min, pl_max, a)
    print(dc)
    print(pl)
