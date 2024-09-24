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

    # Set up the plot
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Real-time BME280 Data')

    # Start the loop to continuously update the plot
    while True:
        # Read the sensor data
        temperature, humidity, pressure = sensor.read()

        # Append the data to the lists
        temperatures.append(temperature)
        humidities.append(humidity)
        pressures.append(pressure)
        times.append(time.time())

        # Clear the previous plot
        ax.clear()

        # Plot the data
        ax.plot(times, temperatures, label='Temperature')
        ax.plot(times, humidities, label='Humidity')
        ax.plot(times, pressures, label='Pressure')

        # Add legend and grid
        ax.legend()
        ax.grid(True)

        # Update the plot
        plt.pause(0.1)

if __name__ == '__main__':
    main()