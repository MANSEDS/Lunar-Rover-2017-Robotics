# MANSEDS Lunar Rover -- Arm Controller
# Author: Ethan Ramsay


# Import dependencies
import argparse
import RPi.GPIO as GPIO
import Adafruit_PCA9685
# import ikpy
import numpy as np
# from ikpy import plot_utils
import logging
import time
from math import sqrt, pow, atan2, cos, sin


# Logging config
logging.basicConfig(filename='arm.log', level=logging.WARNING)


# System variables

### Variables utilising Adafruit PWM hat
## Channels
channel_arm = [0, 1, 2, 3, 4] # Arm servo PWM channels
channel_grip = [5, 6] # Gripper servo PWM channels
## Pulse Length Limits
# Arm servo pl limits
pl_limits_arm = [[150, 750], [150, 750], [150, 750], [150, 750], [150, 750], [150, 750]]
pl_limits_grip = [[160, 600], [160, 600]] # Gripper servo pulse length limits
full_grip_pl = 300
full_release_pl = 580
### Variables using Pi GPIO
## GPIO pins
# pwm_arm = [0, 0, 0, 0, 0] # Arm servo PWM pins
# pwm_grip = [0, 0] # Gripper servo PWM pins
# dc_limits_arm = [[0, 13], [0, 13], [0, 13], [0, 13], [0, 13], [0, 13]] # Arm servo pl limits
# dc_limits_grip = [[0, 13], [0, 13]] # Gripper servo pulse length limits
## Duty Cycle Limits
# full_grip_dc = 7 # Gripper dc at fully closed position
# full_release_dc = 13 # Gripper dc at fully open position
### Arm dimensions
l1 = 150 # Link one is 150 mm long
l2 = 260 # Link two is 260 mm long
l3 = 145 # Link three is 145 mm long
max_radius = l1 + l2
### Preset values
stationary_base_pl = 410
deposit_angles = [102, 140, 140, 180, 140, 5, 45]
### External filenames
base_angle_data_filename = "base_angle.dat" # External file storing base angle value


# Create kinematic chain from URDF file
# lunar_chain = ikpy.chain.Chain.from_urdf_file("arm.urdf")


# GPIO setup
GPIO.setmode(GPIO.BCM)


def GPIO_arm(pwm_arm):
    for pin in pwm_arm:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.PWM(pin, 60)


def GPIO_grip(pwm_grip):
    for pin in pwm_grip:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.PWM(pin, 60)


# Setup Adafruit PWM Hat
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
logging.debug("Adafruit PWM freq set to 60")
# Stop continuous servo from starting
pwm.set_pwm(0, 0, stationary_base_pl)


# Positioning functions
def calc_servo_angles(target_vector):
    logging.warning("Desired gripper position vector: %s", target_vector)
    r = target_vector[0]
    z = target_vector[1] + 145
    target_radius = sqrt(pow(r,2)+pow(z,2))
    logging.warning("r=%s, z=%s, target_radius=%s", r, z, target_radius)
    if target_radius > max_radius:
        raise ValueError('Desired position exceeds reach!')

    # Inverse kinematics solver for 2 link arm
    c2 = (pow(r, 2) + pow(z, 2) - pow(l1, 2) - pow(l2, 2)) / (2 * l1 * l2)
    s2 = sqrt(1 - pow(c2, 2))
    th2_rad = atan2(s2, c2)
    th2 = th2_rad * 180 / 3.142
    k1 = l1 + l2*c2
    k2 = l2 * s2
    th1_rad = atan2(z, r) - atan2(k2, k1)
    th1 = th1_rad * 180 / 3.142

    # for link 3 always downwards
    th3 = 270 - th1 - th2

    servo_angles = [th1, th2, th3]
    logging.warning("Calculated servo angles: %s", servo_angles)
    return servo_angles


def calc_dc(dc_min, dc_max, angle):
    dc_range = dc_max - dc_min
    inter = dc_range * angle / 180
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired servo angle: %s", dc)
    return dc


def calc_pl(pl_min, pl_max, angle):
    if angle > 180:
        raise ValueError("Desired angle exceeds servo range of 180 deg")
    pl_range = pl_max - pl_min
    inter = pl_range * angle / 180
    pl = pl_min + inter
    logging.warning("Calculated required pulse length for desired servo angle: %s", pl)
    pl = int(pl)
    return pl


# Control functions
def extend():
    val = 1
    extended_pl = [0, 0, 0, 0, 0]
    extended_pl[0] = 410
    extended_pl[1] = calc_pl(pl_limits_arm[1][0], pl_limits_arm[1][1], 90)
    extended_pl[2] = extended_pl[1]
    extended_pl[3] = calc_pl(pl_limits_arm[3][0], pl_limits_arm[3][1], 90)
    extended_pl[4] = calc_pl(pl_limits_arm[4][0], pl_limits_arm[4][1], 40)

    # set base rotation to 0 deg
    rotate_arm(0, 0, 0)

    while True:
        pwm.set_pwm(0, 0, extended_pl[0])
        pwm.set_pwm(1, 0, extended_pl[1])
        pwm.set_pwm(2, 0, extended_pl[2])
        pwm.set_pwm(3, 0, extended_pl[3])
        pwm.set_pwm(4, 0, extended_pl[4])
        if val > 0:
            logging.debug("Arm extended")
            val -= 1


def stow():
    val = 1
    while True:
        pwm.set_pwm(0, 0, pl_limits_arm[0][0])
        pwm.set_pwm(1, 0, 300) # pl_limits_arm[1][0])
        pwm.set_pwm(2, 0, 300) # pl_limits_arm[2][0])
        pwm.set_pwm(3, 0, 270) # pl_limits_arm[3][0])
        pwm.set_pwm(4, 0, pl_limits_arm[4][0])
        pwm.set_pwm(5, 0, 240) # pl_limits_grip[0][0])
        pwm.set_pwm(6, 0, pl_limits_grip[1][0])
        if val == 1:
            logging.debug("Arm stowed")
            val -= 1


def deposit_pos():
    val = 1
    deposit_pl = [0, 0, 0, 0, 0, 0, 0]
    deposit_pl[0] = 410
    deposit_pl[1] = calc_pl(pl_limits_arm[1][0], pl_limits_arm[1][1], 130)
    deposit_pl[2] = deposit_pl[1]
    deposit_pl[3] = calc_pl(pl_limits_arm[3][0], pl_limits_arm[3][1], 110)
    deposit_pl[4] = calc_pl(pl_limits_arm[4][0], pl_limits_arm[4][1], 90)
    deposit_pl[5] = calc_pl(pl_limits_grip[0][0], pl_limits_grip[0][1], 5)
    deposit_pl[6] = calc_pl(pl_limits_grip[1][0], pl_limits_grip[1][1], 45)

    # set base rotation to 0
    rotate_arm(0, 0, 0)

    while True:
        pwm.set_pwm(0, 0, deposit_pl[0])
        pwm.set_pwm(1, 0, deposit_pl[1])
        pwm.set_pwm(2, 0, deposit_pl[2])
        pwm.set_pwm(3, 0, deposit_pl[3])
        pwm.set_pwm(4, 0, deposit_pl[4])
        pwm.set_pwm(5, 0, deposit_pl[5])
        time.sleep(2)
        pwm.set_pwm(6, 0, deposit_pl[6])
        if val == 1:
            logging.debug("Gripper positioned above ice box")
            val -= 1


def position_gripper(target_vector):

    a = calc_servo_angles(target_vector)
    pl = [0, 0, 0, 0, 0]
    pl[0] = stationary_base_pl
    pl[1] = calc_pl(pl_limits_arm[1][0], pl_limits_arm[1][1], a[0])
    pl[2] = pl[1]
    pl[3] = calc_pl(pl_limits_arm[3][0], pl_limits_arm[3][1], (180 - a[1]))
    pl[4] = calc_pl(pl_limits_arm[4][0], pl_limits_arm[4][1], a[2])
    val = 1

    while True:
        pwm.set_pwm(0, 0, pl[1])
        pwm.set_pwm(1, 0, pl[1])
        pwm.set_pwm(2, 0, pl[2])
        pwm.set_pwm(3, 0, pl[3])
        pwm.set_pwm(4, 0, pl[4])
        if val == 1:
            logging.warning("Arm position command called for target vector: {}".format(target_vector))
            logging.warning("Calculated pulse lengths to achieve target vector: {}".format(pl))
            val -= 1


def rotate_arm(desired_angle, channel, hold_time):
    if desired_angle > 40 or desired_angle < -40:
        raise ValueError("Desired angle exceeds current configuration range: min = -40 deg; max  \
        = 40 deg")
    current_angle = 0
    with open(base_angle_data_filename, 'r') as f:
        current_angle_str = f.read()
        print("current_angle_str: '" + current_angle_str + "'")
        current_angle = int(current_angle_str)
    print(current_angle)
    perc_full_rot = 100 * abs((desired_angle - current_angle)) / 360
    print(perc_full_rot)
    if desired_angle < current_angle:
        rot_time = ccw_full_rot_time * perc_full_rot / 100
        print(rot_time)
        pwm.set_pwm(channel, 0, 440)
        time.sleep(rot_time)
        pwm.set_pwm(channel, 0, 410)
        with open(base_angle_data_filename, 'w') as f:
            f.write(desired_angle)
        if hold_time != 0:
            time.sleep(hold_time)
    elif desired_angle > current_angle:
        rot_time = ccw_full_rot_time * compensation_factor * perc_full_rot / 100
        pwm.set_pwm(channel, 0, 220)
        time.sleep(rot.time)
        pwm.set_pwm(channel, 0, 410)
        with open(base_angle_data_filename, 'w') as f:
            f.write(desired_angle)
        if hold_time != 0:
            time.sleep(hold_time)
    else:
        pwm.set_pwm(channel, 0, 410)
        if hold_time != 0:
            time.sleep(hold_time)
        # current angle must be equal to desired angle


def grip():
    val = 1
    while True:
        pwm.set_pwm(6, 0, full_grip_pl)
        if val == 1:
            logging.debug("Gripper clamped")
            val -= 1


def drop():
    val = 1
    while True:
        pwm.set_pwm(6, 0, full_release_pl)
        if val == 1:
            logging.debug("Gripper released")
            val -= 1


def worm():
    while True:
        for i in range(0, 400, 1):
            if i < 100:
                pl_1 = 400 - i
            if i > 20 and i < 200:
                pl_1 = 300
                pl_3 = 60 + i
            if i > 200:
                pl_1 = 250
                pl_3 = 400 -i
            if i > 240:
                pl_1 = 250
                pl_3 = 400 - 1
                pl_4 = i
            if i > 320:
                pl_1 = 160 + i
                pl_3 = 160 + 400 - i
                pl_4 = 160 + 400 - i
            pwm.set_pwm(1, 0, pl_1)
            pwm.set_pwm(2, 0, pl_1)


# Main
if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    ge = g.add_mutually_exclusive_group()
    ge.add_argument("-e", "--extend", help="Extend arm", action="store_true")
    ge.add_argument("-s", "--stow", help="Stow arm", action="store_true")
    ge.add_argument("-w", "--wave", help="Do the worm", action="store_true")
    gp = g.add_mutually_exclusive_group()
    gp.add_argument("-r", "--rotate", help="Rotate arm at base (Angle)")
    gp.add_argument("-p", "--position", nargs='+', type=int, help="Gripper Position Vector [radius, height]")
    gp.add_argument("-i", "--icebox", help="Position gripper above ice box to deposit sample", action="store_true")
    gg = g.add_mutually_exclusive_group()
    gg.add_argument("-g", "--grip", help="Grip", action="store_true")
    gg.add_argument("-d", "--drop", help="Release grip", action="store_true")
    args = parser.parse_args()
    e = args.extend
    s = args.stow
    w = args.wave
    if args.rotate:
        r = int(args.rotate)
    r = False
    p = args.position
    i = args.icebox
    g = args.grip
    d = args.drop
    logging.debug("Arguments parsed: e=%s, s=%s, r=%s, p=%s, i=%s, g=%s, d=%s, w=%s", + \
                        e, s, r, p, i, g, d, w)


    if (e or s):
        # GPIO_arm()
        if e:
            extend()
        elif s:
            stow()
    elif ((p or r) or i):
        if p:
            # GPIO_arm()
            r_des = p[0]
            z_des = p[1]
            logging.debug("r_des=%s, z_des=%s", r_des, z_des)
            position_gripper(p)
        elif r:
            rotate_arm(r, 0, 100000)
        elif i:
            deposit_pos()
    elif (g or d):
        # GPIO_grip()
        if g:
            grip()
        elif d:
            drop()
    elif w:
        worm()

# GPIO cleanup
GPIO.cleanup()
