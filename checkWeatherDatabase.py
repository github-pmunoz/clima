import sys
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt

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
    temperatures.append(row[2])
    humidities.append(row[3])

# Create a plot
plt.plot(timestamps, temperatures, label='Temperature')
plt.plot(timestamps, humidities, label='Humidity')

# Customize the plot
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.title('Weather Measurements in the Last 24 Hours')
plt.legend()

# Interpolate the data points
timestamps_interp = np.linspace(min(timestamps), max(timestamps), 100)
temperatures_interp = np.interp(timestamps_interp, timestamps, temperatures)
humidities_interp = np.interp(timestamps_interp, timestamps, humidities)

# Plot the smooth lines
plt.plot(timestamps_interp, temperatures_interp, label='Temperature (Smooth)')
plt.plot(timestamps_interp, humidities_interp, label='Humidity (Smooth)')

# Show the plot
plt.show()