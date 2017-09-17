# MANSEDS Lunar Rover -- Camera Controller
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
import time
import logging


# Logging config
logging.basicConfig(filename='camera.log', level=logging.DEBUG)


# System variables
servo = 0
servo_pwm = 0
servo_dc_limits = [0, 100]
servo_chan = 7
servo_pl_limits = [0, 4095]


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


# Signal functions
def calc_dc(dc_min, dc_max, angle):
    dc_range = dc_max - dc_min
    inter = dc_range * angle / 180
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired extension: %s", dc)
    return dc


def calc_pl(pl_min, pl_max, angle):
    pl_range = pl_max - pl_min
    inter = pl_range * angle / 180
    pl = pl_min + inter
    logging.debug("Calculated required pulse length for desired extension: %s", pl)
    return pl


# Command functions
def pan_GPIO(servo, servo_pwm, servo_dc_limits):
    GPIO_set(servo_pwm, 0)
    for i in range(servo_dc_limits[0], servo_dc_limits[1]+1, 1):
        servo.ChangeDutyCycle(i)
        time.wait(0.01)
    for i in range(servo_dc_limits[1], servo_dc_limits[0]-1, -1):
        servo.ChangeDutyCycle(i)
        time.wait(0.01)
    GPIO_clear(servo)


def pan(servo_chan, servo_pl_limits):
    for i in range(servo_pl_limits[0], servo_pl_limits[1]+1, 16):
        pwm.set_pwm(servo_chan, 0, i)
        time.wait(0.005)
    for i in range(servo_pl_limits[0], servo_pl_limits[1]+1, 16):
        pl = servo_pl_limits[1] - i
        pwm.set_pwm(servo_chan, 0, pl)
        time.wait(0.005)


def move_GPIO(servo, servo_pwm, servo_dc_limits, a):
    dc = calc_dc(servo_dc_limits[0], servo_dc_limits[1], a)
    GPIO_set(servo_pwm, dc)
    GPIO_clear(servo)


def move(servo_chan, servo_pl_limits, a):
    pl = calc_pl(servo_pl_limits[0], servo_pl_limits[1], a)
    pwm.set_pwm(servo_chan, 0, pl)



if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()


    # Command arguments
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("-p", "--pan", help="Pan camera", action="store_true")
    g.add_argument("-m", "--move", help="Move to specific angle (degrees)", action="store_true")


    # Optional arguments
    parser.add_argument("-a", "--angle", help="Camera angle (degrees)")


    # Parse arguments
    args = parser.parse_args()
    p = args.pan
    m = args.move
    a = int(args.angle)

    if p:
        # pan_GPIO(servo, servo_pwm, servo_dc_limits)
        while True:
            pan(servo_chan, servo_pl_limits)

    elif m:
        if a:
            # move_GPIO(servo, servo_pwm, servo_dc_limits, a)
            while True:
                move(servo_chan, servo_pl_limits, a)
        else:
            print("Specify desired camera angle")
