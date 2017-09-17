# MANSEDS Lunar Rover -- Arm Controller
# Author: Ethan Ramsay


# Import dependencies
import argparse
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import ikpy
import numpy as np
from ikpy import plot_utils
import logging


# Logging config
logging.basicConfig(filename='arm.log', level=logging.DEBUG)


# System variables
channel_arm = [0, 1, 2, 3, 4] # Arm servo PWM channels
channel_grip = [5, 6] # Gripper servo PWM channels
pl_limits_arm = [[160, 600], [160, 600], [160, 600], [160, 600], [160, 600], [160, 600]] # Arm servo pl limits
pl_limits_grip = [[160, 600], [160, 600]] # Gripper servo pulse length limits
full_grip_pl = 300 
full_release_pl = 580 
deposit_pl = [400, 400, 400, 400, 400, 400, 300]
pwm_arm = [0, 0, 0, 0, 0] # Arm servo PWM pins
pwm_grip = [0, 0] # Gripper servo PWM pins
dc_limits_arm = [[0, 13], [0, 13], [0, 13], [0, 13], [0, 13], [0, 13]] # Arm servo pl limits
dc_limits_grip = [[0, 13], [0, 13]] # Gripper servo pulse length limits
full_grip_dc = 7 # Gripper dc at fully closed position
full_release_dc = 13 # Gripper dc at fully open position


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


# Positioning functions
def calc_servo_angles(target_vector):
    logging.debug("Desired gripper position vector: %s", target_vector)
    servo_angles = lunar_chain.inverse_kinematics(target_vector)
    logging.debug("Calculated servo angles: %s", servo_angles)
    return servo_angles


def calc_dc(dc_min, dc_max, angle):
    dc_range = dc_max - dc_min
    inter = dc_range * angle / 180
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired servo angle: %s", dc)
    return dc


def calc_pl(pl_min, pl_max, angle):
    pl_range = servo_max - servo_min
    inter = pl_range * angle / 180
    pl = pl_min + inter
    logging.debug("Calculated required pulse length for desired servo angle: %s", pl)
    pl = int(pl)
    return pl


# Control functions
def extend():
    val = 1
    while True:
        pwm.set_pwm(0, 0, pl_limits_arm[0][1])
        pwm.set_pwm(1, 0, pl_limits_arm[1][1])
        pwm.set_pwm(2, 0, pl_limits_arm[2][1])
        pwm.set_pwm(3, 0, pl_limits_arm[3][1]/2)
        pwm.set_pwm(4, 0, pl_limits_arm[4][1]/2)
        pwm.set_pwm(5, 0, pl_limits_grip[0][1]/2)
        pwm.set_pwm(6, 0, pl_limits_grip[1][1]/2)
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
    while True:
        pwm.set_pwm(0, 0, deposit_pl[0])
        pwm.set_pwm(1, 0, deposit_pl[1])
        pwm.set_pwm(2, 0, deposit_pl[2])
        pwm.set_pwm(3, 0, deposit_pl[3])
        pwm.set_pwm(4, 0, deposit_pl[4])
        pwm.set_pwm(5, 0, deposit_pl[5])
        pwm.set_pwm(6, 0, deposit_pl[6])
        if val == 1:
            logging.debug("Gripper positioned above ice box")
            val -= 1


def position_gripper(target_vector):
    a = calc_servo_angles(target_vector)
    pl = [0, 0, 0, 0, 0]
    val = 1
    for i in range(0, 5, 1):
        pl[i] = calc_pl(pl_limits_arm[i][0], pl_limits_arm[i][1], a[i])
    while True:
        for i in range(0, 5, 1):
            pwm.set_pwm(i, 0, pl)
        if val == 1:
            logging.debug("Arm position command called for target vector: {}".format(target_vector))
            logging.debug("Calculated pulse lengths to achieve target vector: {}".format(pl))
            val -= 1


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
    gp.add_argument("-p", "--position", help="Gripper Position Vector")
    gp.add_argument("-i", "--icebox", help="Position gripper above ice box to deposit sample", action="store_true")
    gg = g.add_mutually_exclusive_group()
    gg.add_argument("-g", "--grip", help="Grip", action="store_true")
    gg.add_argument("-d", "--drop", help="Release grip", action="store_true")
    args = parser.parse_args()
    e = args.extend
    s = args.stow
    w = args.wave
    p = args.position # <-- convert from string into ??? format???
    dep = args.icebox
    g = args.grip
    d = args.drop
    logging.debug("Arguments parsed: e=%s, s=%s, z=%s, r=%s, t=%s, g=%s, d=%s", + \
                        e, s, g, d)


    if (e or s):
        # GPIO_arm()
        if e:
            extend()
        elif s:
            stow()
    elif p or dep:
        if p:
            # GPIO_arm()
            position_gripper(p)
        elif dep:
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
