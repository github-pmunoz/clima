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
    ax1 = plt.subplot(3, 1, 1)
    ax2 = plt.subplot(3, 1, 2)
    ax3 = plt.subplot(3, 1, 3)

    # Set the title and labels for the plot
    ax1.set_title('Temperature')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Temperature (°C)')
    ax2.set_title('Humidity')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Humidity (%)')
    ax3.set_title('Pressure')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Pressure (hPa)')
    plt.tight_layout()

    # make the plot in real time
    plt.ion()

    # Start the main loop
    while True:
        # Get the current timestamp
        timestamp = int(time.time())

        # Measure temperature, humidity, and pressure
        temperature, humidity, pressure = sensor.read()

        # Print the data to the console
        print(f"Timestamp: {timestamp}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure}hPa")
        print()

        # Store the data in the lists
        temperatures.append(temperature)
        humidities.append(humidity)
        pressures.append(pressure)
        times.append(timestamp)

        # Plot the data
        ax1.plot(times, temperatures, color='r')
        ax2.plot(times, humidities, color='g')
        ax3.plot(times, pressures, color='b')

        # Pause for a short interval
        plt.show()
        plt.pause(0.1)

if __name__ == '__main__':
    main()