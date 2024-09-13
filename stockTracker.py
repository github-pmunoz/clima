import requests
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt

def get_bitcoin_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    data = response.json()
    price = data['bpi']['USD']['rate_float']
    return price

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

class LED:
        def __init__(self, pin):
            self.pin = pin
            
        def flash(self, times, speed):
            print(f'Flashing LED on pin {self.pin} {times} times at speed {speed}')

class SemaphoreLED:
    def __init__(self, red_pin, yellow_pin, green_pin):
        self.leds = {
            'red': LED(red_pin),
            'yellow': LED(yellow_pin),
            'green': LED(green_pin)
        }
    
# Object that has a handle for a SemaphoreLED (mock for now)
# and turns on the lights based on the Price to EMA ratio
class EMA_Indicator:
    def __init__(self):
        self.lights = {
            "fast": SemaphoreLED(22, 24, 27),
            "mid": SemaphoreLED(23, 25, 28),
            "slow": SemaphoreLED(26, 29, 30)
        }

    def update(self, price, slow_ema, mid_ema, fast_ema):
        if slow_ema is not None:
            slow_ema_ratio = (price / slow_ema - 1.0) * 100.0
            if slow_ema_ratio < 0:
                print(f'\033[91mSlow EMA ratio: {slow_ema_ratio}\033[0m')
            else:
                print(f'\033[92mSlow EMA ratio: {slow_ema_ratio}\033[0m')

            if slow_ema_ratio < 0:
                self.lights["slow"].leds["red"].flash(3, 2)
            elif slow_ema_ratio == 0:
                self.lights["slow"].leds["yellow"].flash(3, 2)
            else:
                self.lights["slow"].leds["green"].flash(3, 2)

        if mid_ema is not None:
            mid_ema_ratio = (price / mid_ema - 1.0) * 100.0
            if mid_ema_ratio < 0:
                print(f'\033[91mMid EMA ratio: {mid_ema_ratio}\033[0m')
            else:
                print(f'\033[92mMid EMA ratio: {mid_ema_ratio}\033[0m')

            if mid_ema_ratio < 0:
                self.lights["mid"].leds["red"].flash(3, 2)
            elif mid_ema_ratio == 0:
                self.lights["mid"].leds["yellow"].flash(3, 2)
            else:
                self.lights["mid"].leds["green"].flash(3, 2)
        
        if fast_ema is not None:
            fast_ema_ratio = (price / fast_ema - 1.0) * 100.0
            if fast_ema_ratio < 0:
                print(f'\033[91mFast EMA ratio: {fast_ema_ratio}\033[0m')
            else:
                print(f'\033[92mFast EMA ratio: {fast_ema_ratio}\033[0m')

            if fast_ema_ratio < 0:
                self.lights["fast"].leds["red"].flash(3, 2)
            elif fast_ema_ratio == 0:
                self.lights["fast"].leds["yellow"].flash(3, 2)
            else:
                self.lights["fast"].leds["green"].flash(3, 2)

bitcoin_prices = []
timestamps = []
slow_emas = []
mid_emas = []
fast_emas = []

plt.ion()  # Turn on interactive mode for real-time plotting

fig, ax = plt.subplots()

indicator = EMA_Indicator()

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

    indicator.update(price, slow_ema[-1], mid_ema[-1], fast_ema[-1])

    time.sleep(15)