# MANSEDS Lunar Rover -- Continuous Servo Controller
# Author: Ethan Ramsay

# Abbreviations:
# dc = duty cycle
# pl = pulse length
# pin = pulse width modulation pin no.

# Import dependencies
import RPi.GPIO as GPIO
import logging
import Adafruit_PCA9685
import time


# Logging config
logging.basicConfig(filename='servo.log', level=logging.WARNING)

# System variables
pi = 3.14159
servo = 0
arm_angle = 0 # degrees
zero_motion_pl = 410
compensation_factor = 1.027
ccw_full_rot_time = 1.1 # s / 360 deg
base_angle_data_filename = "base_angle.dat" # External file storing base angle value


# GPIO setup function
def GPIO_set(pin, dc):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)
    servo.start(dc)


def GPIO_clear(servo):
    servo.stop()
    GPIO.cleanup()


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Funcs
def determine_zero_pl(pl_min, pl_max, channel):
    mid_range_pl = (pl_min + pl_max)/2
    initial_pl = mid_range_pl - 100
    pl = int(initial_pl)
    while pl < (mid_range_pl+100):
        pwm.set_pwm(channel, 0, pl)
        print(pl)
        pl += 10
        time.sleep(1)


def speed_loop(pl_min, pl_max, channel):
    pwm.set_pwm(channel,0,410)
    time.sleep(2)
    pwm.set_pwm(channel,0,440)
    time.sleep(1.1)
    pwm.set_pwm(channel,0,410)
    time.sleep(5)
    pwm.set_pwm(channel,0,220)
    time.sleep(1.1297)
    pwm.set_pwm(channel,0,410)
    time.sleep(5)


def rotational_positioning(desired_angle, channel):
    if desired_angle > 45 or desired_angle < -45:
        raise ValueError("Desired angle exceeds current configuration range: min = -45 deg; max  \
        = 45 deg")
    current_angle = 0
    with open(base_angle_data_filename, 'r') as f:
        current_angle = f.read()
    print(current_angle)
    perc_full_rot = 100 * (desired_angle - current_angle) / 360
    print(perc_full_rot)
    if desired_angle < current_angle:
        rot_time = ccw_full_rot_time * perc_full_rot / 100
        print(rot_time)
        pwm.set_pwm(channel, 0, 440)
        time.sleep(rot_time)
        pwm.set_pwm(channel, 0, 410)
        with open(base_angle_data_filename, 'w') as f:
            f.write(desired_angle)
        time.sleep(100000)
    elif desired_angle > current_angle:
        rot_time = ccw_full_rot_time * compensation_factor * perc_full_rot / 100
        pwm.set_pwm(channel, 0, 220)
        time.sleep(rot.time)
        pwm.set_pwm(channel, 0, 410)
        with open(base_angle_data_filename, 'w') as f:
            f.write(desired_angle)
        time.sleep(1000000)
    else:
        pass # cuurent angle must be equal to desired angle


if __name__ == "__main__":
    while True:
        import argparse

        # Arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("angle", help="Angle of turn (deg)")
        parser.add_argument("direction", help="Direction of turn - True = CCW")

        # Arguments for direct GPIO control from Pi
        # parser.add_argument("dc_min", help="Minimum Duty Cycle")
        # parser.add_argument("dc_max", help="Maximum Duty Cycle")
        # parser.add_argument("pin", help="PWM Pin No. (BCM)")

        # Arguments for Adafruit PWM hat control
        parser.add_argument("pl_min", help="Minimum Pulse Length")
        parser.add_argument("pl_max", help="Maximum Pulse Length")
        parser.add_argument("channel", help="Channel No. (Adafruit PWM Hat)")

        # Parse arguments
        args = parser.parse_args()
        angle = int(args.angle)
        direction = args.direction
        # dc_min = float(args.dc_min)
        # dc_max = float(args.dc_max)
        # pin = int(args.pin)
        pl_min = float(args.pl_min)
        pl_max = float(args.pl_max)
        channel = int(args.channel)
        logging.warning("Channel: %s", channel)

        # Actuate servo
        # GPIO_set(pin, dc)
        # GPIO_clear()

        rotational_positioning(direction, angle, channel)
