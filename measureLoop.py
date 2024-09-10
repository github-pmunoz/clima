import time
import Adafruit_DHT

import matplotlib.pyplot as plt

# Set up the sensor
sensor = Adafruit_DHT.DHT11
pin = 23

# Define the ranges for temperature and humidity
temperature_range = (0, 65)  # Minimum and maximum temperature values
humidity_range = (20, 100)  # Minimum and maximum humidity values

# Initialize lists to store temperature, humidity, and time data
temperature_data = []
humidity_data = []
time_data = []

# Semaphore light
semaphore_light = False

# Function to update the semaphore light
def update_semaphore_light(humidity):
    global semaphore_light
    if humidity > 50:
        semaphore_light = True
    else:
        semaphore_light = False

# Update the semaphore light
update_semaphore_light(20)

# Create the figure and axes for the plots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Temperature plot
axs[0, 0].set_title('Temperature')
axs[0, 0].set_xlabel('Time')
axs[0, 0].set_ylabel('Temperature (°C)')
line_temp, = axs[0, 0].plot([], [], 'b-')

# Humidity plot
axs[0, 1].set_title('Humidity')
axs[0, 1].set_xlabel('Time')
axs[0, 1].set_ylabel('Humidity (%)')
line_humidity, = axs[0, 1].plot([], [], 'g-')

# Temperature vs Humidity plot
axs[1, 0].set_title('Temperature vs Humidity')
axs[1, 0].set_xlabel('Temperature (°C)')
axs[1, 0].set_ylabel('Humidity (%)')
scatter_temp_humidity = axs[1, 0].scatter([], [], c='r', marker='o')

# Semaphore light plot
axs[1, 1].set_title('Semaphore Light')
semaphore_color = 'green' if semaphore_light else 'red'
semaphore_light_patch = axs[1, 1].add_patch(plt.Rectangle((0, 0), 1, 1, facecolor=semaphore_color))

fig.plot()

# Main loop
while True:
    # Read the sensor data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # Check if data is within the defined ranges
    if temperature < temperature_range[0] or temperature > temperature_range[1] or \
            humidity < humidity_range[0] or humidity > humidity_range[1]:
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

        # Update the semaphore light
        update_semaphore_light(humidity)
        semaphore_color = 'green' if semaphore_light else 'red'
        semaphore_light_patch.set_facecolor(semaphore_color)
    
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
