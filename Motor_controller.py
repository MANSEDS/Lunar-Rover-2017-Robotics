# Controller for Motors in the MANSEDS Lunar Rover
# Author: Ethan Ramsay

# Import dependencies
import RPi.GPIO as GPIO
from scipy.constants import pi as pi


# Set GPIO pin configuration
GPIO.setmode(GPIO.BOARD)


# Declare motor pins
motor_pwm_pins = []
motor_hilo_pins = [[][][][]]
GPIO.setup(motor_pins, GPIO.OUT)


# Define motor instance
def motor_instance(motor_number):
    motor_inst(motor_number) = GPIO.PWM(motor_pwm_pins[motor_number], 50)


# Define motor angular velocity control
motor_duty_cycles = [[],[]]
max_rpm = 26
max_ang_vel = max_rpm * 2 * pi #rad/s
wheel_diameter = 0.1 #m


def velocity_converter(motor_number, velocity):
  duty_cycle_limits = motor_duty_cycles[motor_number]
  duty_cycle_range = duty_cycle_limits[1] - duty_cycle_limits[0]
  desired_ang_vel = wheel_diameter*pi
  desired_duty_cycle = desired_ang_vel/max_ang_vel*duty_cycle_range+duty_cycle_limits[0]
  return desired_duty_cycle


#Define speed controller
def velocity_controller(motor_number, velocity):
    motor_instance(motor_number)
    dc = velocity_converter(motor_number, velocity)
    return motor_instance(motor_number).start(dc)


def motor_brake:
    for motor in motor_pins:
        motor_instance(motor)
