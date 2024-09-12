import requests
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

# for each of the emas (slow, mid, fast) we have a green-yellow-red led light
GPIO.setmode(GPIO.BCM)
pins = {
    'slow': {
        'red': 13,
        'yellow': 11,
        'green': 12
    },  
    'mid': {
        'red': 22,
        'yellow': 23,
        'green': 24
    },
    'fast': {
        'red': 20,
        'yellow': 26,
        'green': 21
    }
}
for ema, colors in pins.items():
    for color, pin in colors.items():
        GPIO.setup(pin, GPIO.OUT)
        

def turn_on_led(pin):
    GPIO.output(pin, GPIO.HIGH)

def turn_off_led(pin):
    GPIO.output(pin, GPIO.LOW)

def flash_led(pin, times):
    for _ in range(times):
        turn_off_led(pin)
        turn_on_led(pin)
        time.sleep(0.5)
        turn_off_led(pin)
        time.sleep(0.5)

def get_bitcoin_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    data = response.json()
    price = data['bpi']['USD']['rate_float']
    return price

def ema_indicator(price, ema, pins, flash=0):
    # if the price is near to the EMA, turn on yellow LED. If the price is above the EMA, turn on green LED. If the price is below the EMA, turn on red LED.
    # use a level of tolerance for the price to be considered near the EMA
    if ema is None:
        return
        
    tolerance = 0.1
    if flash:
        flash_led(pins['red'], flash)

    if price < ema * (1 - tolerance):
        turn_on_led(pins['red'])
    elif price > ema * (1 + tolerance):
        turn_on_led(pins['green'])
    else:
        turn_on_led(pins['yellow'])

def calculate_ema(prices, window):
    if(len(prices) < window):
        return [None]

    # calculate the EMA for the given window
    ema = []
    k = 2 / (window + 1)
    ema.append(np.mean(prices[:window]))
    for i in range(window, len(prices)):
        ema.append(prices[i] * k + ema[-1] * (1 - k))
    return ema

def calculate_emas(bitcoin_prices):
    slow_ema = calculate_ema(bitcoin_prices, 30)
    mid_ema = calculate_ema(bitcoin_prices, 15)
    fast_ema = calculate_ema(bitcoin_prices, 5)
    return slow_ema, mid_ema, fast_ema

bitcoin_prices = []
timestamps = []
slow_emas = []
mid_emas = []
fast_emas = []

plt.ion()  # Turn on interactive mode for real-time plotting

fig, ax = plt.subplots()

while True:
    price = get_bitcoin_price()
    bitcoin_prices.append(price)
    slow_ema, mid_ema, fast_ema = calculate_emas(bitcoin_prices)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamps.append(timestamp)
    slow_emas.append(slow_ema[-1])
    mid_emas.append(mid_ema[-1])
    fast_emas.append(fast_ema[-1])

    ax.clear()  # Clear the previous plot
    ax.plot(timestamps, bitcoin_prices, label='Price')
    ax.plot(timestamps, slow_emas, label='Slow EMA')
    ax.plot(timestamps, mid_emas, label='Mid EMA')
    ax.plot(timestamps, fast_emas, label='Fast EMA')
    ax.legend()

    plt.xticks([])

    plt.draw()  # Redraw the plot
    plt.pause(0.1)  # Pause to allow the plot to update

    if slow_ema[-1] is not None:
        slow_ema_ratio = (price / slow_ema[-1] - 1.0) * 100.0
        if slow_ema_ratio < 0:
            print(f'\033[91mSlow EMA ratio: {slow_ema_ratio}\033[0m')
        else:
            print(f'\033[92mSlow EMA ratio: {slow_ema_ratio}\033[0m')

    if mid_ema[-1] is not None:
        mid_ema_ratio = (price / mid_ema[-1] - 1.0) * 10000.0
        if mid_ema_ratio < 0:
            print(f'\033[91mMid EMA ratio: {mid_ema_ratio}\033[0m')
        else:
            print(f'\033[92mMid EMA ratio: {mid_ema_ratio}\033[0m')

    if fast_ema[-1] is not None:
        fast_ema_ratio = (price / fast_ema[-1] - 1.0) * 10000.0
        if fast_ema_ratio < 0:
            print(f'\033[91mFast EMA ratio: {fast_ema_ratio}\033[0m')
        else:
            print(f'\033[92mFast EMA ratio: {fast_ema_ratio}\033[0m')

    print("")

    # Use led flash indicators with the last prices and emas
    ema_indicator(price, slow_ema[-1], pins['slow'], flash=1)
    ema_indicator(price, mid_ema[-1], pins['mid'], flash=2)
    ema_indicator(price, fast_ema[-1], pins['fast'], flash=3)

    time.sleep(15)