# Controller for Robotic Arm of MANSEDS Lunar Rover
# Author: Ethan Ramsay

# Import dependencies
import RPi.GPIO as GPIO
from scipy.constants import pi as pi
import time
from Servo_controller import servo_controller

# System variables
max_z = 0
min_z = 0
max_r = 0
min_r = 0
max_t = 360
min_t = 0
# determine rest angle (base servo)
# determine neutral angle (base servo)
# determine safe height (gripper)



# Functions for extending and stowing arm
def extend:
    # turn base to appropriate position (Neutral Angle)

    # raise gripper above height of all rover mounted systems (Safe height)

    # half extend to a neutral position

    pass


def stow:
    # raise gripper above height of all rover mounted systems (Safe height)
    # turn base to appropriate position (Neutral Angle)
    # stow arm
    # rotate base to rest position (Rest Angle)
    pass

# Functions for positioning the gripper
def rposition(r):
    if r > r_max or r < r_min:
        raise ValueError('Desired radial position outside of system range')
    pass


def tposition(t):
    i = 0
    while t > t_max:
        t = t - 360
        i++
        if i >10:
            break
    pass


def zposition(z):
    if z > z_max or z < z_min:
        raise ValueError('Desired height outside of system range')
    pass


# Functions for gripping/releasing samples
def grip:
    gripper_servo_number = 7
    return servo_controller(gripper_servo_number, 180, 180)

def release:
    gripper_servo_number = 7
    return servo_controller(gripper_servo_number, 0, 180)
