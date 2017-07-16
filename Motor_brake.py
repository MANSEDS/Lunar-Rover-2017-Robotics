# MANSEDS Lunar Rover -- Motor Controller
# Author: Ethan Ramsay


# Import dependencies
import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685
import logging


# System variables
motor_hilo_pins= [[0, 0], [0, 0], [0, 0], [0, 0]]


# GPIO setup
GPIO.setmode(GPIO.BCM)


# Motor brake function
def motor_brake():
    for pins in motor_hilo_pins:
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(True)


if __name__ == "__main__":
    motor_brake()
