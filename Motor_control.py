# Controller for Motors in the Drive System of the MANSEDS Lunar Rover

# Import dependencies
import RPi.GPIO as GPIO
import time

# Set GPIO pin configuration
GPIO.setmode(GPIO.BOARD)


# Declare motor pins
motor_pins = []
GPIO.setup(motor_pins, GPIO.OUT)


# Define motor instance
def motor_instance(motor_number):
    motor_1 = GPIO.PWM(motor_pins[motor_number], 50)
    return motor_1


# Define motor angular velocity calculator
motor_duty_cycles = [[], [], [], [], []]


def angular_velocity_convertor(motor_number, angular_velocity):
max_angular_velocity = 0
    duty_cycle_limits = servo_duty_cycles[servo_number-1]
    duty_cycle_range = duty_cycle_limits[1] - duty_cycle_limits[0]
    if max_degree == 180:
        desired_duty_cycle = degree * duty_cycle_range / 180 + duty_cycle_limits[0]
    elif max_degree ==360:
        desired_duty_cycle = degree * duty_cycle_range / 360 + duty_cycle_limits[0]
    else:
        raise ValueError('Maximum degree not equal to 180 or 360')
    return desired_duty_cycle


# Define motor controller
def servo_controller(servo_number, degree):
    dc = degree_converter(servo_number,degree, 180)
    servo_instance(servo_number).start(dc)
