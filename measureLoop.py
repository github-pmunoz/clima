#!/usr/bin/env python
import time
import Adafruit_DHT

# Set up the sensor
sensor = Adafruit_DHT.DHT11
pin = 23

# Main loop
fails = 0
while True:
    # Read the sensor data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Check if data was successfully retrieved
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature}°C \t Humidity: {humidity}%")
    else:
        print("Failed to retrieve data from sensor")
        fails += 1
        if fails > 5:
            print("Too many failed attempts. Exiting...")
            break

    # Wait for 0.25 seconds before the next measurement
    time.sleep(0.25)