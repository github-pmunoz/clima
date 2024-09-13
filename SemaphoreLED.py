#!/usr/bin/env python

"""
This is a Python script for controlling GPIO pins.
"""
import RPi.GPIO as GPIO
import time
import argparse
import multiprocessing

class LED:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def flash(self, times, speed):
        for _ in range(times):
            self.turn_off()
            self.turn_on()
            time.sleep(1.0/speed)
            self.turn_off()
            time.sleep(1.0/speed)

class SemaphoreLED:
    def __init__(self, red_pin, yellow_pin, green_pin):
        self.lights = {
            'red': LED(red_pin),
            'yellow': LED(yellow_pin),
            'green': LED(green_pin)
        }

    def flash(self, times, speed):
        # Flash the lights using multiprocessong and then join the processes
        subprocesses = []
        for light in self.lights.values():
            p = multiprocessing.Process(target=light.flash, args=(times, speed))
            p.start()
            subprocesses.append(p)
        for p in subprocesses:
            p.join()

    def xmas_tree(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            self.flash(3, 2)
            self.flash(3, 4)
            self.flash(1, 10)

"""
Usage:
python SemaphoreLED.py --red 22 --yellow 24 --green 27
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--red', type=int, required=True)
    parser.add_argument('--yellow', type=int, required=True)
    parser.add_argument('--green', type=int, required=True)
    args = parser.parse_args()

    try:
        GPIO.setmode(GPIO.BCM)
        semaphore = SemaphoreLED(args.red, args.yellow, args.green)
        semaphore.xmas_tree(10)
    finally:   
        GPIO.cleanup()
    