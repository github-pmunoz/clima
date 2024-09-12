import Adafruit_DHT
import time

import RPi.GPIO as GPIO

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up the LED pins
RED_PIN = 22
YELLOW_PIN = 24
GREEN_PIN = 27

# Initialize LED pins as output
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

# Initialize DHT11 sensor
sensor = Adafruit_DHT.DHT11
pin = 23

def measure_temperature_humidity():
    # Read temperature and humidity from DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        return None, None

def update_led(weather):
    # Turn off all LEDs
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)

    # Update LED based on weather
    if weather == "nice":
        GPIO.output(GREEN_PIN, GPIO.HIGH)
    elif weather == "warm":
        GPIO.output(YELLOW_PIN, GPIO.HIGH)
    elif weather == "hot":
        GPIO.output(RED_PIN, GPIO.HIGH)

try:
    while True:
        temperature, humidity = measure_temperature_humidity()
        print(temperature, humidity)

        if temperature is not None and humidity is not None:
            # Categorize the temperature on green (nice), yellow (warm), or red (hot)
            if temperature <= 24:
                weather = "nice"
            elif temperature <= 30:
                weather = "warm"
            else:
                weather = "hot"

            update_led(weather)

            print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Weather: {weather}")
        else:
            print("Failed to read data from DHT11 sensor")

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()
