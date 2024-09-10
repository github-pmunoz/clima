import time
import Adafruit_DHT

#!/usr/bin/env python
import matplotlib.pyplot as plt

# Set up the sensor
sensor = Adafruit_DHT.DHT11
pin = 23

# Initialize lists to store temperature and time data
temperature_data = []
time_data = []

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot(time_data, temperature_data)
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Real-time Temperature')

# Main loop
fails = 0
while True:
    # Read the sensor data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Check if data was successfully retrieved
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.6f}°C \t Humidity: {humidity:.6f}%")  # Print with 6 decimal accuracy
        temperature_data.append(temperature)
        time_data.append(time.time())  # Use current time as x-axis value

        # Update the plot
        line.set_data(time_data, temperature_data)
        ax.relim()
        ax.autoscale_view()

        # Redraw the plot
        fig.canvas.draw()
        fig.canvas.flush_events()
    else:
        print("Failed to retrieve data from sensor")
        fails += 1
        if fails > 5:
            print("Too many failed attempts. Exiting...")
            break

    # Wait for 0.25 seconds before the next measurement
    time.sleep(0.01)
