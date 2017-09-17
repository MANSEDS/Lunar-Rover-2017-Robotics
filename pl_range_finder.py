# MANSEDS Lunar Rover -- Pulse Length Range Finder
# Author: Ethan Ramsay

import argparse
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time

# Arguments
parser = argparse.ArgumentParser()
t = parser.add_mutually_exclusive_group(required=True)
t.add_argument("-m", "--motor", action="store_true")
t.add_argument("-s", "--servo", action="store_true")
t.add_argument("-l", "--linact", action="store_true")
parser.add_argument("channel", help="Channel no. (Adafruit Board)")
parser.add_argument("frequency", help="Frequency (Hz)")
parser.add_argument("-a", "--high", help="Motor high pin no. (BOARD)")
parser.add_argument("-b", "--low", help="Motor low pin no. (BOARD)")
args = parser.parse_args()
m = args.motor
s = args.servo
l = args.linact
channel = int(args.channel)
f = int(args.frequency)
if (args.high and args.low):
    hi = int(args.high)
    lo = int(args.low)


# GPIO setup
GPIO.setmode(GPIO.BCM)
def GPIO_motor(hi, lo):
    GPIO.setup(hi, GPIO.OUT)
    GPIO.setup(lo, GPIO.OUT)
    GPIO.output(hi, 1)
    GPIO.output(lo, 0)


# Adafruit setup
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(f)


# Pulse length range finder
def pl_range_finder(channel):
    for pl in range(0, 4096, 16):
        pwm.set_pwm(channel, 0, pl)
        print(pl)
        time.sleep(1)


# Run range finder
print("Running pulse length range finder, press Ctrl+C to break")
if m:
    if (hi and lo):
        GPIO_motor(hi, lo)
        pl_range_finder(channel)
    else:
        print("Specify motor high and low pins")
elif s:
    pl_range_finder(channel)
elif l:
    pl_range_finder(channel)

# GPIO clean up
GPIO.cleanup()
