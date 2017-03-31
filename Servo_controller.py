# Controller for Servos in the Robotic Arm of the MANSEDS Lunar Rover

# Import dependencies
import RPi.GPIO as GPIO


# Set GPIO pin configuration
GPIO.setmode(GPIO.BOARD)


# Declare servo pins
servo_pins = []
GPIO.setup(servo_pins, GPIO.OUT)


# Define servo instance
def servo_instance(servo_number):
    servo_1 = GPIO.PWM(servo_pins[servo_number], 50)


# Define degree converter
servo_duty_cycles = [[], [], [], [], []]


def degree_converter(servo_number, degree, max_degree):
    duty_cycle_limits = servo_duty_cycles[servo_number]
    duty_cycle_range = duty_cycle_limits[2] - duty_cycle_limits[1]
    if max_degree == 180:
        desired_duty_cycle = degree * duty_cycle_range / 180 + duty_cycle_limits[1]
    elif max_degree ==360:
        desired_duty_cycle = degree * duty_cycle_range / 180 + duty_cycle_limits[1]
    else:
        raise ValueError('Maximum degree not equal to 180 or 360')
    return desired_duty_cycle


# Define servo controller
def servo_controller(servo_number, degree):
    servo_instance(servo_number)
    dc = degree_converter(servo_number,degree)
    servo_instance.start(dc)


