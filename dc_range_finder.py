import argparse
import RPi.GPIO as GPIO
import time

# Arguments
parser = argparse.ArgumentParser()
t = parser.add_mutually_exclusive_group(required=True)
t.add_argument("-m", "--motor", action="store_true")
t.add_argument("-s", "--servo", action="store_true")
t.add_argument("-l", "--linact", action="store_true")
parser.add_argument("PWM", help="PWM pin no. (BOARD)")
parser.add_argument("frequency", help="Frequency (Hz)")
parser.add_argument("-a", "--high", help="Motor high pin no. (BOARD)")
parser.add_argument("-b", "--low", help="Motor low pin no. (BOARD)")
args = parser.parse_args()
m = args.motor
s = args.servo
l = args.linact
pwm_pin = int(args.PWM)
f = int(args.frequency)
hi = int(args.high)
lo = int(args.low)


# GPIO setup
GPIO.setmode(GPIO.BOARD)
inst = GPIO.PWM(pwm_pin, f)
def GPIO_motor(hi, lo):
    GPIO.output(hi, 1)
    GPIO.output(lo, 0)

# Duty cycle range finder
def dc_range_finder(inst):
    inst.start(0)
    for dc in range(1, 101, 1):
        inst.ChangeDutyCycle(dc)
        print(dc)
        time.sleep(2)
    inst.stop()


# Run range finder
if m:
    if (hi and lo):
        GPIO_motor(hi, lo)
        dc_range_finder(inst)
    else:
        print("Specify motor high and low pins")
elif s:
    dc_range_finder(inst)
elif l:
    dc_range_finder(inst)

# GPIO clean up
GPIO.cleanup()
