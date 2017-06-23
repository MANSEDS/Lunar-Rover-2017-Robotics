# Controller for Servos in the MANSEDS Lunar Rover
# Author: Ethan Ramsay

# Import dependencies
import RPi.GPIO as GPIO
from scipy.constants import pi as pi


# Set GPIO pin configuration
GPIO.setmode(GPIO.BOARD)


# Declare servo pins
servo_pins = [12]
GPIO.setup(servo_pins, GPIO.OUT)


# Define servo instance
def servo_instance(servo_number):
    servo_instance(servo_number) = GPIO.PWM(servo_pins[servo_number], 50)


# Define degree converter
servo_duty_cycles = [[5, 10], [], [], [], [], [], []]


def degree_converter(servo_number, degree, max_degree):
    duty_cycle_limits = servo_duty_cycles[servo_number]
    duty_cycle_range = duty_cycle_limits[1] - duty_cycle_limits[0]
    if max_degree == 180:
        desired_duty_cycle = degree * duty_cycle_range / 180 + duty_cycle_limits[1]
    elif max_degree ==360:
        desired_duty_cycle = degree * duty_cycle_range / 180 + duty_cycle_limits[1]
    else:
        raise ValueError('Maximum degree not equal to 180 or 360')
    return desired_duty_cycle


# Define servo controller
def servo_controller(servo_number, degree, max degree):
    servo_instance(servo_number)
    dc = degree_converter(servo_number,degree, max_degree)
    return servo_instance(servo_number).start(dc)
