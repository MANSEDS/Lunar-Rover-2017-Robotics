# MANSEDS Lunar Rover -- Continuous Servo Controller
# Author: Ethan Ramsay

# Abbreviations:
# dc = duty cycle
# pl = pulse length
# pin = pulse width modulation pin no.

# Import dependencies
import RPi.GPIO as GPIO
import logging
import Adafruit_PCA9685
import time


# Logging config
logging.basicConfig(filename='servo.log', level=logging.WARNING)

# System variables
pi = 3.14159
servo = 0
arm_angle = 0 # degrees

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
def determine_zero_pl(pl_min, pl_max):
    mid_range_pl = (pl_min + pl_max)/2
    initial_pl = mid_range_pl - 100
    pl = int(initial_pl)
    while pl < (mid_range_pl+100):
        pwm.set_pwm(channel, 0, pl)
        print(pl)
        pl + 10
        time.sleep(1)


def speed_loop():
    pass


if __name__ == "__main__":
    while True:
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
        logging.warning("Channel: %s", channel)

        # Actuate servo
        # GPIO_set(pin, dc)
        # GPIO_clear()
        pwm.set_pwm(channel, 0, pl)
