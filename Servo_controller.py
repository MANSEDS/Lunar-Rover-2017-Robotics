# MANSEDS Lunar Rover -- Servo Controller
# Author: Ethan Ramsay

# Import dependencies
import RPi.GPIO as GPIO
import logging


# Logging config
logging.basicConfig(filename='servo.log', level=logging.DEBUG)

# System variables
wheel_diameter = 0.12 # m
pi = 3.14159
max_rpm = 26
max_ang_vel = max_rpm * pi / 30 # rad/s
servo = 0

# GPIO setup function
def GPIO_set(pwm, dc):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwm, GPIO.OUT)
    servo = GPIO.PWM(pwm, 50)
    servo.start(dc)


def GPIO_clear(servo):
    servo.stop()
    GPIO.cleanup()


def calc_dc(dc_min, dc_max, angle):
    dc_range = dc_max - dc_min
    inter = dc_range * angle / 180
    dc = dc_min + inter
    return dc


if __name__ == "__main__":

    import argparse

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("a", help="Angle (Degrees)")
    parser.add_argument("pwm", help="PWM pin no.")
    parser.add_argument("dc_min", help="Minimum Duty Cycle")
    parser.add_argument("dc_max", help="Maximum Duty Cycle")
    args = parser.parse_args()
    a = float(args.a)
    pwm = int(args.pwm)
    dc_min = float(args.dc_min)
    dc_max = float(args.dc_max)
    if args.od:
        overdrive = True
        print("Overdrive enabled, not recommended for extended durations")
    else:
        overdrive = False


    # Calculate interpolated duty cycle
    dc = calc_dc(dc_min, dc_max, a)
    GPIO_set(pwm, dc)
    GPIO_clear(servo)

else:
    des_ang_vel = calc_des_ang_vel(v)
    dc = calc_dc
    print(dc)
