import time
import sqlite3
from DHT11 import DHT11

# Define the pin number for the DHT11 sensor
DHT_PIN = 4
sensor = DHT11(DHT_PIN)

# Define the time interval between measurements (in seconds)
MEASUREMENT_INTERVAL = 60

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS measurements
             (timestamp INTEGER, temperature REAL, humidity REAL)''')

# Function to store the measurement in the database
def store_measurement(timestamp, temperature, humidity):
    c.execute("INSERT INTO measurements VALUES (?, ?, ?)", (timestamp, temperature, humidity))
    conn.commit()

# Main loop
while True:
    # Get the current timestamp
    timestamp = int(time.time())

    # Measure temperature and humidity
    humidity, temperature = sensor.measure()

    # Store the measurement in the database
    store_measurement(timestamp, temperature, humidity)

    # Wait for the next measurement
    time.sleep(MEASUREMENT_INTERVAL)

# Close the database connection
conn.close()