import smbus2
import bme280
import time

import matplotlib.pyplot as plt

class BME280:
    def __init__(self, address=0x76, bus=1):
        self.address = address
        self.bus = smbus2.SMBus(bus)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def read_temperature(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.temperature

    def read_humidity(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.humidity

    def read_pressure(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.pressure

    def read(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.temperature, data.humidity, data.pressure

def main():
    sensor = BME280()

    # Initialize empty lists to store data
    temperatures = []
    humidities = []
    pressures = []
    times = []

    # Create a figure and axes for the plot
    fig, ax = plt.subplots()

    # Set up the plot on different subplots for each variable and each pair of variables in a 3x3 grid
    # Avoid the repetition of the same plot (only do upper-left triangle)
    for i, var1 in enumerate(['temperature', 'humidity', 'pressure']):
        for j, var2 in enumerate(['temperature', 'humidity', 'pressure']):
            if i >= j:
                continue
            ax = plt.subplot(3, 3, 3 * i + j + 1)
            ax.set_xlabel(var1)
            ax.set_ylabel(var2)

    # Main loop
    while True:
        # Get the current timestamp
        timestamp = time.time()

        # Measure temperature, humidity, and pressure
        temperature, humidity, pressure = sensor.read()

        # Print the data
        print(f"Timestamp: {timestamp}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print()

        # Store the data
        temperatures.append(temperature)
        humidities.append(humidity)
        pressures.append(pressure)
        times.append(timestamp)

        # Update the plot
        for i, var1 in enumerate(['temperature', 'humidity', 'pressure']):
            for j, var2 in enumerate(['temperature', 'humidity', 'pressure']):
                if i >= j:
                    continue
                ax = plt.subplot(3, 3, 3 * i + j + 1)
                ax.plot(times, temperatures, label='temperature', color='red')
                ax.plot(times, humidities, label='humidity', color='blue')
                ax.plot(times, pressures, label='pressure', color='green')
                ax.legend()

        plt.pause(0.01)