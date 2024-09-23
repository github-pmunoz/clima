import sys
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Path, Arrow
from matplotlib.collections import LineCollection
from scipy.interpolate import interp1d

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
# always start after 09-21-2024
start_time = max(int(datetime.datetime(2024, 9, 21, 0, 0, 0).timestamp()), int(datetime.datetime.now().timestamp()) - days * 24 * 60 * 60)
rows = queryDatabase(filename, start_time)

# convert the timestamps to chilean time
rows = [(row[0] - 3*60*60, row[1], row[2]) for row in rows]

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

# use a large screen size
fig, axs = plt.subplots(2, 2, figsize=(20, 10))
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

def plotResults(ax, x, y, title, xlabel, ylabel):
    ax.plot(x, y, linewidth=2)
    ax.set_facecolor('0.1')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.xlim = (min(x), max(x))
    # make the x-axis ticks more readable (just use the month, date and hour)
    # just use regular hours for the x-axis (00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
    ax.xaxis.set_major_locator(plt.MultipleLocator(4*60*60))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda value, tick_number: datetime.datetime.fromtimestamp(value).strftime('%m-%d %H:%M')))
    #rotate the x-axis labels to make them more readable
    ax.xaxis.set_tick_params(rotation=90)
    #move the ticks to the left so that the end of the tick label is at meets the edge at the tick
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_position('bottom')
    #add vertical lines separing the days
    for i in range(1, len(x)):
        if datetime.datetime.fromtimestamp(x[i]).day != datetime.datetime.fromtimestamp(x[i-1]).day:
            ax.axvline(x[i], color='0.5', linestyle='--')
    #add the date on top of the vetical line
    for i in range(1, len(x)):
        if datetime.datetime.fromtimestamp(x[i]).day != datetime.datetime.fromtimestamp(x[i-1]).day:
            ax.text(x[i], max(y), datetime.datetime.fromtimestamp(x[i]).strftime('%m-%d'), verticalalignment='bottom', horizontalalignment='center', color='0.5')
    
    

# Line plot of temperature vs time
plotResults(axs[0, 1], ema_timestamps, ema_temperature, 'Temperature vs Time', 'Time', 'Temperature (°C)')
# Line plot of humidity vs time
plotResults(axs[1, 0], ema_timestamps, ema_humidity, 'Humidity vs Time', 'Time', 'Humidity (%)')

# In 1,1 plot the derivative of the ema_temperature vs time
# Calculate the derivative of the temperature
gradient_window = 360
derivative = np.gradient(ema_temperature, ema_timestamps)
derivative = np.convolve(derivative, np.ones(gradient_window)/gradient_window, mode='valid')
derivative_timestamps = np.convolve(ema_timestamps, np.ones(gradient_window)/gradient_window, mode='valid')

# Plot the derivative
axs[1, 1].plot(derivative_timestamps, derivative, linewidth=2)
axs[1, 1].set_facecolor('0.1')
axs[1, 1].set_xlabel('Time')
axs[1, 1].set_ylabel('Derivative of Temperature')
axs[1, 1].set_title('Derivative of Temperature vs Time')
axs[1, 1].xlim = (min(derivative_timestamps), max(derivative_timestamps))
# make the x-axis ticks more readable (just use the month, date and hour)
# just use regular hours for the x-axis (00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
axs[1, 1].xaxis.set_major_locator(plt.MultipleLocator(4*60*60))
axs[1, 1].xaxis.set_major_formatter(plt.FuncFormatter(lambda value, tick_number: datetime.datetime.fromtimestamp(value).strftime('%m-%d %H:%M')))
#rotate the x-axis labels to make them more readable
axs[1, 1].xaxis.set_tick_params(rotation=90)
#move the ticks to the left so that the end of the tick label is at meets the edge at the tick
axs[1, 1].xaxis.set_ticks_position('bottom')
axs[1, 1].xaxis.set_label_position('bottom')
#add vertical lines separing the days
for i in range(1, len(derivative_timestamps)):
    if datetime.datetime.fromtimestamp(derivative_timestamps[i]).day != datetime.datetime.fromtimestamp(derivative_timestamps[i-1]).day:
        axs[1, 1].axvline(derivative_timestamps[i], color='0.5', linestyle='--')
#add the date on top of the vetical line
for i in range(1, len(derivative_timestamps)):
    if datetime.datetime.fromtimestamp(derivative_timestamps[i]).day != datetime.datetime.fromtimestamp(derivative_timestamps[i-1]).day:
        axs[1, 1].text(derivative_timestamps[i], max(derivative), datetime.datetime.fromtimestamp(derivative_timestamps[i]).strftime('%m-%d'), verticalalignment='bottom', horizontalalignment='center', color='0.5')
#draw a dashed line at y=0
axs[1, 1].axhline(0, color='0.5', linestyle='--')
#fill the area above and below the line with different colors (red for top and cyan for bottom)
axs[1, 1].fill_between(derivative_timestamps, derivative, 0, where=derivative>0, color='red', alpha=0.5)
axs[1, 1].fill_between(derivative_timestamps, derivative, 0, where=derivative<0, color='cyan', alpha=0.5)
#add vertical dashed-dotted lines when the derivative changes sign
#after a change of sign, the next one needs to be at least 1 hour later
for i in range(1, len(derivative)):
    if derivative[i] * derivative[i-1] < 0 and derivative_timestamps[i] - derivative_timestamps[i-1] > 70:
        axs[1, 1].axvline(derivative_timestamps[i], color='0.5', linestyle='-.')
        axs[1, 1].text(derivative_timestamps[i], max(derivative), datetime.datetime.fromtimestamp(derivative_timestamps[i]).strftime('%H-%M'), verticalalignment='bottom', horizontalalignment='center', color='0.5')


# Adjust the layout
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# Show the plot
plt.show()