import time
import Adafruit_DHT

import matplotlib.pyplot as plt

# Set up the sensor
sensor = Adafruit_DHT.DHT11
pin = 23

# Initialize lists to store temperature, humidity, and time data
temperature_data = []
humidity_data = []
time_data = []

# Set up the plot
fig, axs = plt.subplots(2, 2)
fig.suptitle('Real-time Climate Data')

# Temperature plot
axs[0, 0].set_xlabel('Time')
axs[0, 0].set_ylabel('Temperature (°C)')
axs[0, 0].set_title('Temperature')
line_temp, = axs[0, 0].plot(time_data, temperature_data)
axs[0, 0].set_ylim(0, 65)  # Set the y-axis limits for temperature plot

# Humidity plot
axs[0, 1].set_xlabel('Time')
axs[0, 1].set_ylabel('Humidity (%)')
axs[0, 1].set_title('Humidity')
line_humidity, = axs[0, 1].plot(time_data, humidity_data)
axs[0, 1].set_ylim(0, 100)  # Set the y-axis limits for humidity plot

# Temperature vs Humidity plot
axs[1, 0].set_xlabel('Temperature (°C)')
axs[1, 0].set_ylabel('Humidity (%)')
axs[1, 0].set_title('Temperature vs Humidity')
scatter_temp_humidity = axs[1, 0].scatter(temperature_data, humidity_data)
axs[1, 0].set_xlim(0, 65)  # Set the x-axis limits for temperature vs humidity plot
axs[1, 0].set_ylim(0, 100)  # Set the y-axis limits for temperature vs humidity plot

# Hide the empty subplot
axs[1, 1].axis('off')

# Main loop
fails = 0
fig.show()
while True:
    # Read the sensor data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # check range is correct to discard outliers
    if temperature < 0 or temperature > 65 or humidity < 0 or humidity > 100:
        print("Out of range values. Discarding...")
        continue

    # Check if data was successfully retrieved
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.6f}°C \t Humidity: {humidity:.6f}%")  # Print with 6 decimal accuracy
        temperature_data.append(temperature)
        humidity_data.append(humidity)
        time_data.append(time.time())  # Use current time as x-axis value

        # Update the temperature plot
        line_temp.set_data(time_data, temperature_data)
        axs[0, 0].relim()
        axs[0, 0].autoscale_view()

        # Update the humidity plot
        line_humidity.set_data(time_data, humidity_data)
        axs[0, 1].relim()
        axs[0, 1].autoscale_view()

        # Update the temperature vs humidity plot
        scatter_temp_humidity.set_offsets(list(zip(temperature_data, humidity_data)))

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
