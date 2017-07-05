# MANSEDS Lunar Rover -- Motor Controller
# Author: Ethan Ramsay


# Import dependencies
import RPi.GPIO as GPIO
import time
import logging


# Logging config
logging.basicConfig(filename='motor.log', level=logging.DEBUG)


# System variables
wheel_diameter = 0.12 # m
pi = 3.14159
max_rpm = 26
max_ang_vel = max_rpm * pi / 30 # rad/s
motor = 0


# GPIO setup/functions/cleanup
def GPIO_set(pwm, dc):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwm, GPIO.OUT)
    motor = GPIO.PWM(pwm, 50)
    motor.start(dc)


def GPIO_clear(motor):
    motor.stop()
    GPIO.cleanup()


# Calculate angular velocity for desired velocity
def calc_des_ang_vel(v):
    des_ang_vel = 2 * v / wheel_diameter # rad/s
    if des_ang_vel > max_ang_vel:
        if od:
            des_ang_vel = max_ang_vel
            print("Desired velocity exceeds maximum velocity, velocity set to maximum due to" + \
                                "overdrive, extended use of overdrive is not recommended")
        else:
            des_ang_vel = max_ang_vel * 0.9
    elif des_ang_vel >= 0.9 * max_ang_vel:
        if not od:
            des_ang_vel = 0.9 * max_ang_vel
    return des_ang_vel


def calc_dc(dc_min, dc_max, des_ang_vel):
    dc_range = dc_max - dc_min
    inter = dc_range * des_ang_vel / max_ang_vel
    dc = dc_min + inter
    return dc


if __name__ == "__main__":

    import argparse

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("v", help="Velocity (m/s)")
    parser.add_argument("t", hgelp="Operation time (s)")
    parser.add_argument("dc_min", help="Minimum Duty Cycle")
    parser.add_argument("dc_max", help="Maximum Duty Cycle")
    parser.add_argument("--od", help="Overdrive Enable", action="store_true")
    args = parser.parse_args()
    v = float(args.v)
    t = float(args.t)
    dc_min = float(args.dc_min)
    dc_max = float(args.dc_max)
    od = args.od
    if args.od:
        print("Overdrive enabled, not recommended for extended durations")

    # Calculate angular velocity for desired velocity
    des_ang_vel = calc_des_ang_vel(v)
    print("Desired angular velocity is: "+str(des_ang_vel))


    # Calculate interpolated duty cycle
    dc_range = dc_max - dc_min
    inter = dc_range * des_ang_vel / max_ang_vel
    dc = dc_min + inter
    print("Required duty cycle is: "+str(dc))

    GPIO_set(pwm, dc)
    time.sleep(t)
    GPIO_clear()

else:
    des_ang_vel = calc_des_ang_vel(v)
    dc = calc_dc
    print(dc)
