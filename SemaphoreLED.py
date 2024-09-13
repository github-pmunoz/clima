#!/usr/bin/env python

"""
This is a Python script for controlling GPIO pins.
"""
import RPi.GPIO as GPIO
import time
import argparse
import multiprocessing
import random

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
        self.status = 'red'

    def on(self, duration, sleep_time):
        #Launch a subprocess with a function that uses update_light logic to cycle through the lights
        def run():
            start_time = time.time()
            while time.time() - start_time < duration:
                self.update_light()
                time.sleep(sleep_time)
        p = multiprocessing.Process(target=run)
        p.start()
        p.join()
    
    def update_light(self):
        self.stop()
        if self.status == 'red':
            self.status = 'yellow'
        elif self.status == 'yellow':
            self.status = 'green'
        elif self.status == 'green':
            self.status = 'red'
        self.start()

    def flash(self, times, speed):
        # Flash the lights using multiprocessong and then join the processes
        subprocesses = []
        for light in self.lights.values():
            p = multiprocessing.Process(target=light.flash, args=(times, speed))
            p.start()
            subprocesses.append(p)
        for p in subprocesses:
            p.join()

    def random_light(self, delay, total_time):
        def run():
            start_time = time.time()
            while time.time() - start_time < total_time:
                for light in self.lights.values():
                    if random.random() < 0.5:
                        light.turn_on()
                    else:
                        light.turn_off()
                    time.sleep(delay)
        subprocesses = []
        for light in self.lights.values():
            p = multiprocessing.Process(target=run)
            p.start()
            subprocesses.append(p)
        for p in subprocesses:
            p.join()

    def xmas_tree(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            self.flash(3, 2)
            self.random_light(0.5, 3)
            self.flash(3, 4)
            self.random_light(0.25, 2)
            self.flash(1, 10)
            self.random_light(0.1, 1)

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
        semaphore.on(10, 0.1)
            
    finally:   
        GPIO.cleanup()
    