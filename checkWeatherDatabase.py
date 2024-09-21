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
    temperatures.append(row[1])
    humidities.append(row[2])

# Create a plot
plt.plot(timestamps, temperatures, label='Temperature')
plt.plot(timestamps, humidities, label='Humidity')

# Customize the plot
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.title('Weather Measurements in the Last 24 Hours')
plt.legend()

# Interpolate the data points using an exponential moving average
temperatures = np.array(temperatures)
humidities = np.array(humidities)

# Calcular la media móvil
moving_average = np.convolve(temperatures, np.ones(24)/24, mode='valid')

# Calcular la desviación estándar móvil
moving_std = np.array([np.std(temperatures[i - 23 : i + 1]) for i in range(23, len(temperatures))])

# Calcular las bandas de Bollinger
bollinger_upper = moving_average + 2 * moving_std
bollinger_lower = moving_average - 2 * moving_std

# Asegurarse de que las longitudes de los timestamps y las bandas de Bollinger coinciden
timestamps = timestamps[23:]
min_length = min(len(timestamps), len(bollinger_upper), len(bollinger_lower))
bollinger_upper = bollinger_upper[:min_length]
bollinger_lower = bollinger_lower[:min_length]
temperature_std = moving_std[:min_length]
temperatures = temperatures[23:]  # Corrected spelling of variable name

# Plot the Bollinger Bands
plt.plot(timestamps, moving_average, label='Moving Average')
plt.plot(timestamps, bollinger_upper, label='Upper Bollinger Band')
plt.plot(timestamps, bollinger_lower, label='Lower Bollinger Band')
plt.fill_between(timestamps, bollinger_lower, bollinger_upper, alpha=0.2)

# Plot the interpolated data
plt.plot(timestamps, temperatures, label='Temperature (Interpolated)')
plt.fill_between(timestamps, temperatures - temperature_std, temperatures + temperature_std, alpha=0.2)

# Show the plot
plt.show()