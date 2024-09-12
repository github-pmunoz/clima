import time
import requests

import RPi.GPIO as GPIO

# Set up GPIO pins for the lights
RED_PIN = 22
YELLOW_PIN = 24
GREEN_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

def get_bitcoin_price():
    # Make a request to the API to get the current Bitcoin price
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    data = response.json()
    price = data['bpi']['USD']['rate']
    return float(price.replace(',', ''))

def update_lights(price):
    # Update the lights based on the price
    if price > 0.001:
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif price == 0.001:
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(YELLOW_PIN, GPIO.HIGH)
        GPIO.output(RED_PIN, GPIO.LOW)
    else:
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)

try:
    while True:
        price = get_bitcoin_price()
        update_lights(price)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()