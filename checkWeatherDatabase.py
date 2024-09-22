import sys
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt

def sigmaClipping(data, threshold=3):
    mean = np.mean(data)
    std = np.std(data)
    data = np.array([value if abs(value - mean) < threshold * std else np.nan for value in data])
    std = np.std(data)
    while std > threshold * std:
        mean = np.mean(data)
        data = np.array([value if abs(value - mean) < threshold * std else np.nan for value in data])
        std = np.std(data)
    return data

# Get the filename argument from the shell
filename = sys.argv[1]

# Query the database for measurements in the last 24 hours that are not null values
conn = sqlite3.connect(filename)
cursor = conn.cursor()
query = "SELECT * FROM measurements WHERE timestamp > ? AND temperature IS NOT NULL AND humidity IS NOT NULL"
start_time = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())
cursor.execute(query, (start_time,))
rows = cursor.fetchall()
cursor.close()
conn.close()

# Extract the temperature and humidity values
timestamps = []
temperatures = []
humidities = []
for row in rows:
    timestamps.append(row[0])
    temperatures.append(row[1])
    humidities.append(row[2])

# Interpolate the data points using an exponential moving average
temperatures = np.array(temperatures)
humidities = np.array(humidities)

# Remove outliers using sigma clipping
temperatures = sigmaClipping(temperatures)
humidities = sigmaClipping(humidities)

# Exponential moving average for temperature and humidity
moving_average_window = 12
ema_temperature = np.convolve(temperatures, np.ones(moving_average_window)/moving_average_window, mode='valid')
ema_humidity = np.convolve(humidities, np.ones(moving_average_window)/moving_average_window, mode='valid')

# Plot the temperature and humidity data (Ema only) 
# use a 2x2 grid of subplots
# (1, 1) is scatter plot of temperature vs humidity
# (1, 2) is line plot of temperature vs time
# (2, 1) is line plot of humidity vs time
# (2, 2) is empty
fig, axs = plt.subplots(2, 2)
fig.suptitle('Temperature and Humidity Data')
# 2D hexagonal hist of temperature vs humidity
axs[0, 0].hexbin(ema_temperature, ema_humidity, gridsize=50, cmap='viridis')
axs[0, 0].set_xlabel('Temperature (°C)')
axs[0, 0].set_ylabel('Humidity (%)')
# Line plot of temperature vs time
axs[0, 1].plot(ema_temperature)
axs[0, 1].set_xlabel('Time')
axs[0, 1].set_ylabel('Temperature (°C)')
# Line plot of humidity vs time
axs[1, 0].plot(ema_humidity)
axs[1, 0].set_xlabel('Time')
axs[1, 0].set_ylabel('Humidity (%)')
# Empty plot
axs[1, 1].axis('off')
# Adjust the layout
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# Show the plot
plt.show()