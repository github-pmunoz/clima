import time
import random

import RPi.GPIO as GPIO

# Set up the LED pins
red_pin = 22
yellow_pin = 24
green_pin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# Function to randomly turn lights on and off
def random_light(delay, total_time):
    start_time = time.time()
    while time.time() - start_time < total_time:
        # Randomly turn on and off the lights
        if random.random() < 0.5:
            GPIO.output(red_pin, GPIO.HIGH)
        else:
            GPIO.output(red_pin, GPIO.LOW)
        if random.random() < 0.5:
            GPIO.output(yellow_pin, GPIO.HIGH)
        else:
            GPIO.output(yellow_pin, GPIO.LOW)
        if random.random() < 0.5:
            GPIO.output(green_pin, GPIO.HIGH)
        else:
            GPIO.output(green_pin, GPIO.LOW)
        time.sleep(delay)

while True:
    random_light(0.5, 3)
    random_light(0.25, 2)
    random_light(0.1, 1)