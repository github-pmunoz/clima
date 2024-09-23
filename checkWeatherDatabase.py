import sys
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Path, Arrow
from matplotlib.collections import LineCollection
from scipy.interpolate import interp1d

def sigmaClipping(data, threshold=5):
    mean = np.mean(data)
    std = np.std(data)
    data = np.array([value if abs(value - mean) < threshold * std else np.nan for value in data])
    std = np.std(data)
    while std > threshold * std:
        mean = np.mean(data)
        data = np.array([value if abs(value - mean) < threshold * std else np.nan for value in data])
        std = np.std(data)
    return data

def queryDatabase(filename, start_time):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    query = "SELECT * FROM measurements WHERE timestamp > ? AND temperature IS NOT NULL AND humidity IS NOT NULL"
    cursor.execute(query, (start_time,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Get the filename argument from the shell
filename = sys.argv[1]

# Get the number of days to plot from the shell (default is all 1 month)
if len(sys.argv) > 2:
    days = int(sys.argv[2])
else:
    days = 30

# Query the database for measurements in the last 'days' days
start_time = int((datetime.datetime.now() - datetime.timedelta(days=days)).timestamp())
rows = queryDatabase(filename, start_time)

# Extract the temperature and humidity values
timestamps = []
temperatures = []
humidities = []
for row in rows:
    timestamps.append(row[0])
    temperatures.append(row[1])
    humidities.append(row[2])

# Remove outliers using sigma clipping
temperatures = np.array(temperatures)
humidities = np.array(humidities)
temperatures = sigmaClipping(temperatures)
humidities = sigmaClipping(humidities)

# Exponential moving average for temperature and humidity
moving_average_window = 25
ema_temperature = np.convolve(temperatures, np.ones(moving_average_window)/moving_average_window, mode='valid')
ema_humidity = np.convolve(humidities, np.ones(moving_average_window)/moving_average_window, mode='valid')
ema_timestamps = np.convolve(timestamps, np.ones(moving_average_window)/moving_average_window, mode='valid')

# Plot the temperature and humidity data (Ema only) 
# use a 2x2 grid of subplots
# (1, 1) is scatter plot of temperature vs humidity
# (1, 2) is line plot of temperature vs time
# (2, 1) is line plot of humidity vs time
# (2, 2) is empty
fig, axs = plt.subplots(2, 2)
fig.suptitle('Temperature and Humidity Data')

# Scatter plot of temperature vs humidity using a gradient of colors for distinguishing the time
# Convert the timestamps to a gradient of colors using a black background
colors = np.array(ema_timestamps) - min(ema_timestamps)
colors = colors / max(colors)
colors = plt.cm.plasma(colors)

# Create the scatter plot on dark gray background, and fill the interior of the polygon formed by the data points
axs[0, 0].scatter(ema_humidity, ema_temperature, color=colors)
axs[0, 0].set_facecolor('0.1')
axs[0, 0].set_ylabel('Temperature (°C)')
axs[0, 0].set_xlabel('Humidity (%)')
axs[0, 0].ylim = (min(ema_temperature), max(ema_temperature))
axs[0, 0].xlim = (min(ema_humidity), max(ema_humidity))

axs[0, 1].plot(ema_timestamps, ema_temperature, color='red')
axs[0, 1].set_facecolor('0.1')
axs[0, 1].set_xlabel('Time')
axs[0, 1].set_ylabel('Temperature (°C)')
axs[0, 1].xlim = (min(ema_timestamps), max(ema_timestamps))
axs[0, 1].ylim = (min(ema_temperature), max(ema_temperature))

axs[1, 0].plot(ema_timestamps, ema_humidity, color='cyan')
axs[1, 0].set_facecolor('0.1')
axs[1, 0].set_xlabel('Time')
axs[1, 0].set_ylabel('Humidity (%)')
axs[1, 0].xlim = (min(ema_timestamps), max(ema_timestamps))
axs[1, 0].ylim = (min(ema_humidity), max(ema_humidity))

axs[1, 1].axis('off')

# Adjust the layout
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# Show the plot
plt.show()