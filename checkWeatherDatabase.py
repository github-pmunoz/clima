import sys
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Path, Arrow

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
moving_average_window = 50
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
colors = plt.cm.viridis(colors)

# Create the scatter plot
scatter = axs[0, 0].scatter(ema_temperature, ema_humidity, c=colors)

# add on top arrows on direction of the path given by time
scatter_path = Path(np.array([ema_temperature, ema_humidity]).T)
scatter_path_patch = PathPatch(scatter_path, facecolor='none', edgecolor='none')
axs[0, 0].add_patch(scatter_path_patch)
for i in range(len(ema_temperature) - 1):
    arrow = Arrow(ema_temperature[i], ema_humidity[i], ema_temperature[i + 1] - ema_temperature[i], ema_humidity[i + 1] - ema_humidity[i], color=colors[i], alpha=0.5)
    axs[0, 0].add_patch(arrow)

# Add colorbar
cbar = plt.colorbar(scatter, ax=axs[0, 0])
cbar.set_label('Time')
cbar.set_ticks([0, 1])
cbar.set_ticklabels(['Start', 'End'])


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