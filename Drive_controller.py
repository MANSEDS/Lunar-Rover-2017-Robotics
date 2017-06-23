# Drive controller for the MANSEDS Lunar Rover Project
# Author: Ethan Ramsay

# Import dependencies
from . import Motor_controller
import time
from scipy.constants import pi as pi


# System variables
wheel_base = 200 #mm ?Guess - needs precise measurement?
tyre_diameter = 80 #mm ?Guess - needs precise value?


# Define steering control
def steering_control(degree):
    m0 = motor_instance(0)
    m1 = motor_instance(1)
    turn_velocity = 0
    # maths to calculate time duration to achieve desired turn angle
    # circle of diameter = distance between midlines of tyre banks
    turning_circle_circumference = wheel_base * pi
    # vehicle moves around circle 1 tyre circumference per revolution
    tyre_circumference = pi * tyre_diameter
    #
    # look at wheel radius, velocity
    turn_time =
    velocity_controller(0, -turn_velocity)
    velocity_controller(1, turn_velocity)
    time.wait(turn_time)


# Define drive control
def drive_control(velocity, distance):
    m0 = motor_instance(0)
    m1 = motor_instance(1)
    drive_time = distance / velocity
    velocity_controller(0, velocity)
    velocity_controller(1, velocity)
    time.wait(drive_time)
