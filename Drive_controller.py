# MANSEDS Lunar Rover -- Drive Controller
# Author: Ethan Ramsay


# Import dependencies
import argparse
import RPi.GPIO as GPIO
import time
import logging


# Logging config
logging.basicConfig(filename='drive.log', level=logging.DEBUG)
# Set index



# Arguments
parser = argparse.ArgumentParser()


# Command arguments
g = parser.add_mutually_exclusive_group(required=True)
gd = g.add_mutually_exclusive_group()
gd.add_argument("-f", "--forward", help="Drive forwards", action="store_true")
gd.add_argument("-b", "--backwards", help="Drive backwards", action="store_true")
gt = g.add_mutually_exclusive_group()
gt.add_argument("-l", "--left", help="Turn left", action="store_true")
gt.add_argument("-r", "--right", help="Turn right", action="store_true")


# Optional arguments
parser.add_argument("-v", "--velocity", help="Drive velocity (m/s)")
parser.add_argument("-d", "--duration", help="Drive duration (s)")parser.add_argument("-d", "--duration", help="Drive duration (s)")
parser.add_argument("-od", "--overdrive", help="Enable overdrive", action="store_true")
parser.add_argument("-a", "--angle", help="Turn Angle (Degrees)")

# Parse arguments
args = parser.parse_args()
f = args.forward
b = args.backwards
l = args.left
r = args.right
v = float(args.velocity)
d = float(args.duration)
overdrive = args.overdrive
a = int(args.angle)
logging.debug("Arguments parsed: f=%s, b=%s, l=%s, r=%s, v=%s, d=%s, od=%s, a=%s", + \
                    f, b, l, r, v, d, od, a)


# System variables
pi = 3.14159
wheel_diameter = 0.12 # m
wheel_width = 0.06 # m
axle_diameter = 0.0254 # m
axle_length = 0.14 # m
wheel_base = 0.1524 # m
max_rpm = 26.0
max_ang_vel = max_rpm * pi / 30 # rad/s
motor_pwm_pins = [0, 0, 0, 0]
motor_channels = [8, 9, 10, 11]
motor_hilo_pins = [[0, 0], [0, 0], [0, 0], [0, 0]]
motor_dc_limits = [[0, 100], [0, 100], [0, 100], [0, 100]]
motor_pl_limits = [[0, 4095], [0, 4095], [0, 4095], [0, 4095]]
motor_insts = []


# GPIO setup
GPIO.setmode(GPIO.BOARD)
# for i in range(0, 4, 1):
#     GPIO.setup(motor_pwm_pins, GPIO.OUT)
#     motor_insts.append(GPIO.PWM(motor_pwm_pins[i], 50))


def GPIO_forward():
    for i in range(0, 4, 1):
        GPIO.setup(motor_hilo_pins[i], GPIO.OUT)
        GPIO.output(motor_hilo_pins[i[0]], 1)
        GPIO.output(motor_hilo_pins[i[1]], 0)


def GPIO_backwards():
    for i in range(0,4,1):
        GPIO.setup(motor_hilo_pins[i], GPIO.OUT)
        GPIO.output(motor_hilo_pins[i[1]], 1)
        GPIO.output(motor_hilo_pins[i[0]], 0)


def GPIO_left():
    for i in range(0,4,2):
        GPIO.setup(motor_hilo_pins[i], GPIO.OUT)
        GPIO.output(motor_hilo_pins[i[0]], 1)
        GPIO.output(motor_hilo_pins[i[1]], 0)
    for i in range(1,4,2):
        GPIO.setup(motor_hilo_pins[i], GPIO.OUT)
        GPIO.output(motor_hilo_pins[i[1]], 1)
        GPIO.output(motor_hilo_pins[i[0]], 0)


def GPIO_right():
    for i in range(0,4,2):
        GPIO.setup(motor_hilo_pins[i], GPIO.OUT)
        GPIO.output(motor_hilo_pins[i[1]], 1)
        GPIO.output(motor_hilo_pins[i[0]], 0)
    for i in range(1,4,2):
        GPIO.setup(motor_hilo_pins[i], GPIO.OUT)
        GPIO.output(motor_hilo_pins[i[0]], 1)
        GPIO.output(motor_hilo_pins[i[1]], 0)


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
logging.debug('Set Adafruit pwm freq to 60')


# Calculate angular velocity for desired velocity
def calc_des_ang_vel(v):
    des_ang_vel = 2 * v / wheel_diameter # rad/s
    if des_ang_vel > max_ang_vel:
        if overdrive:
            des_ang_vel = max_ang_vel
            print("Desired velocity exceeds maximum velocity, velocity set to maximum due to" + \
                                "overdrive, extended use of overdrive is not recommended")
        else:
            des_ang_vel = max_ang_vel * 0.9
    elif des_ang_vel >= 0.9 * max_ang_vel:
        if not overdrive:
            des_ang_vel = 0.9 * max_ang_vel
    return des_ang_vel


# Calculate duty cycle for velocity
def calc_dc(dc_min, dc_max, des_ang_vel):
    dc_range = dc_max - dc_min
    inter = dc_range * des_ang_vel / max_ang_vel
    dc = dc_min + inter
    logging.debug("Calculated required duty cycle for desired angular velocity: %s", dc)
    return dc


# Calculate pulse length for velocity
def calc_pl(pl_min, pl_max, des_ang_vel):
    pl_range = servo_max - servo_min
    inter = pl_range * des_ang_vel / max_ang_vel
    per = inter / pl_range
    pl = pl_min + inter
    logging.debug("Calculated required pulse length for desired angular velocity: %s", pl)
    return pl, per


# Calculate duty cycle for turning at 80% of max velocity
def turn_dc(dc_min, dc_max):
    dc_range = dc_max - dc_min
    inter = dc_range * 0.8
    dc = dc_min + inter
    return dc


# Calculate time to turn by desired angle at 80% of max velocity
def turn_time(a):
    # Calculate turning diameter,d, using pythagarus
    l1 = (axle_length + wheel_width) / 2 # m
    l2 = (axle_diameter + wheel_base) / 2 # m
    d = (l1 ** 2 + l2 ** 2) ** (0.5) # m
    # Calculate angle turned through 1 revolution of tyres
    th = (d / wheel_diameter) * 360 # degrees
    # Calculate number of revolutions to turn by desired angle
    n = a / th # revs
    # Calculate revs/s of wheel at 80% max velocity
    om = max_rpm * 0.8 / 60
    # Calculate turn time
    t = n / om
    return t


# Main control
if (f or b):
    if (v and d):
        des_ang_vel = calc_des_ang_vel(v)
        if f:
            GPIO_forward()
            for i in range(0,4,1):
                # dc = calc_dc(motor_dc_limits[i[0]], motor_dc_limits[i[1]], des_ang_vel)
                # m = motor_insts[i]
                # m.start(dc)
                pl, per = calc_pl((motor_pl_limits[i[0]], motor_pl_limits[i[1]], des_ang_vel))
                pwm.set_pwm(motor_channels[i], 0, pl)
                with open("/var/www/html/drive.dat", "a+") as handle:
                    handle.write("{} {} {}".format(index, 1, per))
                logging.warning("{} {} {}".format(index, 1, per))
                index += 1
            time.sleep(d)
            for i in range(0, 4, 1):
                # m = motor_insts[i]
                # m.stop()
                pwm.set_pwm(motor_channels[i], 0, 0)
        elif b:
            if f:
                GPIO_backwards()
                for i in range(0,4,1):
                    # dc = calc_dc(motor_dc_limits[i[0]], motor_dc_limits[i[1]], des_ang_vel)
                    # m = motor_insts[i]
                    # m.start(dc)
                    pl, per = calc_pl((motor_pl_limits[i[0]], motor_pl_limits[i[1]], des_ang_vel))
                    pwm.set_pwm(motor_channels[i], 0, pl)
                    with open("/var/www/html/drive.dat", "a+") as handle:
                        handle.write("{} {} {}".format(index, -1, per))
                    logging.warning("{} {} {}".format(index, -1, per))
                    index += 1
                time.sleep(d)
                for i in range(0, 4, 1):
                    # m = motor_insts[i]
                    # m.stop()
                    pwm.set_pwm(motor_channels[i], 0, 0)
    else:
        print("Please specify velocity AND duration of travel")
elif (l or r):
    if a:
        while a > 360:
            a -= 360
            i++
            if i > 10:
                print("Specify an angle between 0 and 360 degrees")
                break

        t = turn_time(a)
        if l:
            GPIO_left()
            for i in range(0,4,1):
                # dc = calc_dc(motor_dc_limits[i[0]], motor_dc_limits[i[1]], des_ang_vel)
                # m = motor_insts[i]
                # m.start(dc)
                pl, per = calc_pl((motor_pl_limits[i[0]], motor_pl_limits[i[1]], des_ang_vel))
                pwm.set_pwm(motor_channels[i], 0, pl)
                with open("/var/www/html/drive.dat", "a+") as handle:
                    handle.write("{} {} {}".format(index, 0, per))
                logging.warning("{} {} {}".format(index, 0, per))
                index += 1
            time.sleep(t)
            for i in range(0, 4, 1):
                # m = motor_insts[i]
                # m.stop()
                pwm.set_pwm(motor_channels[i], 0, 0)
        elif b:
            if r:
                GPIO_right()
                for i in range(0,4,1):
                    # dc = calc_dc(motor_dc_limits[i[0]], motor_dc_limits[i[1]], des_ang_vel)
                    # m = motor_insts[i]
                    # m.start(dc)
                    pl, per = calc_pl((motor_pl_limits[i[0]], motor_pl_limits[i[1]], des_ang_vel))
                    pwm.set_pwm(motor_channels[i], 0, pl)
                    per = - per
                    with open("/var/www/html/drive.dat", "a+") as handle:
                        handle.write("{} {} {}".format(index, 0, per))
                    logging.warning("{} {} {}".format(index, 0, per))
                    index += 1
                time.sleep(t)
                for i in range(0, 4, 1):
                    # m = motor_insts[i]
                    # m.stop()
                    pwm.set_pwm(motor_channels[i], 0, 0)
    else:
        print("Please specify angle of turn (degrees)")


# GPIO clean up
GPIO.cleanup()
