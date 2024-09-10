#!/usr/bin/env python
import Adafruit_DHT

# Set the GPIO sensor pin number
pin = 23

# Set the sensor type (DHT11)
sensor = Adafruit_DHT.DHT11

# Try to read the temperature and humidity from the sensor
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Check if the reading was successful
if humidity is not None and temperature is not None:
    print('Temperature: {0:.1f}°C'.format(temperature))
    print('Humidity: {0:.1f}%'.format(humidity))
else:
    print('Failed to retrieve data from the sensor')