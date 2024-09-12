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
    # Get the current Bitcoin price from the CoinDesk API
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    data = response.json()
    price = data['bpi']['USD']['rate_float']
    return price

def get_bitcoin_price_change(last_price):
    # Get the difference between last price and new price
    new_price = get_bitcoin_price()
    price_change = new_price - last_price
    return price_change

def update_lights(price):
    # Update the lights based on the price
    if price > 0:
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif price == 0:
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(YELLOW_PIN, GPIO.HIGH)
        GPIO.output(RED_PIN, GPIO.LOW)
    else price < 0:
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)

try:      
    # Get the current Bitcoin price
    price = get_bitcoin_price()
    time.sleep(0.25)
    while True:
        # Update the lights based on the price change
        price_change = get_bitcoin_price_change(price)
        update_lights(price_change)

        # Wait for 1 second before checking the price again
        time.sleep(0.25)
except KeyboardInterrupt:
    GPIO.cleanup()