# MANSEDS Lunar Rover -- Servo Controller
# Author: Ethan Ramsay

# Import dependencies
import RPi.GPIO as GPIO
import logging
import Adafruit_PCA9685


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


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


# Funcs
def calc_dc(dc_min, dc_max, angle):
    dc_range = dc_max - dc_min
    inter = dc_range * angle / 180
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired angular velocity: %s", dc)
    return dc


def calc_pl(servo_min, servo_max, angle):
    pl_range = servo_max - servo_min
    inter = pl_range * angle / 180
    pl = pl_min + inter
    logging.debug("Calculated required pulse length for desired angular velocity: %s", pl)
    return pl


if __name__ == "__main__":

    import argparse

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("a", help="Angle (Degrees)")

    # Arguments for direct GPIO control from Pi
    # parser.add_argument("dc_min", help="Minimum Duty Cycle")
    # parser.add_argument("dc_max", help="Maximum Duty Cycle")
    # parser.add_argument("pwm", help="PWM Pin No. (BOARD)")

    # Arguments for Adafruit PWM hat control
    parser.add_argument("servo_min", help="Minimum Pulse Length")
    parser.add_argument("servo_max", help="Maximum Pulse Length")
    parser.add_argument("channel", help="Channel No. (Adafruit PWM Hat)")

    # Parse arguments
    args = parser.parse_args()
    a = float(args.a)
    # dc_min = float(args.dc_min)
    # dc_max = float(args.dc_max)
    # pwm = int(args.pwm)
    servo_min = float(args.servo_min)
    servo_max = float(args.servo_max)
    channel = int(args.channel)


    # Calculate interpolated duty cycle
    # dc = calc_dc(dc_min, dc_max, a)

    pl = calc_pl(servo_min, servo_max, a)
    pwm.set_pwm(channel, 0, pl)

else:
    dc = calc_dc(dc_min, dc_max, a)
    pl = calc_pl(servo_min, servo_max, a)
    print(dc)
    print(pl)
