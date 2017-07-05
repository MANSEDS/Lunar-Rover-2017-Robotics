# MANSEDS Lunar Rover -- Servo Controller
# Author: Ethan Ramsay


# Import dependencies
import argparse
import RPi.GPIO as GPIO
import logging


# Logging config
logging.basicConfig(filename='arm.log', level=logging.DEBUG)


# Arguments
parser = argparse.ArgumentParser()
g = parser.add_mutually_exclusive_group(required=True)
ge = g.add_mutually_exclusive_group()
ge.add_argument("-e", "--extend", help="Extend arm", action="store_true")
ge.add_argument("-s", "--stow", help="Stow arm", action="store_true")
gp = g.add_mutually_exclusive_group()
gp.add_argument("-z", "--height", help="Position gripper - height")
gp.add_argument("-r", "--radius", help="Position gripper - radius")
gp.add_argument("-t", "--theta", help="Position gripper - theta")
gg = g.add_mutually_exclusive_group()
gg.add_argument("-g", "grip", help="Grip", action="store_true")
gg.add_argument("-d", "drop", help="Release grip", action="store_true")
args = parser.parse_args()
e = args.extend
s = args.stow
z = float(args.height)
r = float(args.radius)
t = int(args.theta)
g = args.grip
d = args.drop


# System variables
pwm_arm = [0, 0, 0, 0, 0, 0] # Arm servo PWM pins
pwm_grip = [0, 0] # Gripper servo PWM pins
dc_limits_arm = [[0 100], [0 100], [0 100], [0 100], [0 100], [0 100]]
dc_limits_grip = [[0 100], [0 100]]
servo_insts = []


# GPIO setup
GPIO.setmode(GPIO.BOARD)
# requires command to set pwm pins to output


def GPIO_grip():
    GPIO.setup(pwm_grip, GPIO.OUT)
    for pin in pwm_grip:
        servo_insts.append(GPIO.PWM(pin, 50))


def GPIO_arm():
    GPIO.setup(pwm_arm, GPIO.OUT)
    for pin in pwm_arm:
        servo_insts.append(GPIO.PWM(pin, 50))


# Control functions
def extend():
    pass


def stow():
    pass


def position(dim, mag):
    pass


def grip():
    for i in range(0,2,1):
        servo_insts[i].start(duty_limits_grip[i[1]])


def drop():
    for i in range(0,2,1):
        servo_insts[i].start(duty_limits_grip[i[0]])


# Main
if (e or s):
    GPIO_arm()
    if e:
        extend()
    elif s:
        stow()
elif (z or r or t):
    GPIO_arm()
    pass # inverse kinematics
elif (g or d):
    GPIO_grip()
    if g:
        grip()
    elif d:
        drop()


# GPIO clean up
GPIO.cleanup()
