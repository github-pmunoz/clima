import time
import sqlite3
from DHT11 import DHT11
from BME280 import BME280

# Define the pin number for the DHT11 dht11
DHT_PIN = 27
dht11 = DHT11(DHT_PIN)

# Define the I2C address for the BME280 dht11
BME280_ADDRESS = 0x76
bme280 = BME280(BME280_ADDRESS)

SENSORS = {
    'DHT11': dht11,
    'BME280': bme280
}

# Define the time interval between measurements (in seconds)
MEASUREMENT_INTERVAL = 60

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS measurements
             (timestamp INTEGER, temperature REAL, humidity REAL, pressure REAL, dht11 TEXT)''')

# Function to store the measurement in the database
def store_measurement(timestamp, temperature, humidity, pressure, dht11):
    if dht11 == 'DHT11':
        store_dht11_measurement(timestamp, temperature, humidity)
    elif dht11 == 'BME280':
        store_bme280_measurement(timestamp, temperature, humidity, pressure)

def store_dht11_measurement(timestamp, temperature, humidity):
    c.execute("INSERT INTO measurements VALUES (?, ?, ?, NULL, 'DHT11')", (timestamp, temperature, humidity))
    conn.commit()

def store_bme280_measurement(timestamp, temperature, humidity, pressure):
    c.execute("INSERT INTO measurements VALUES (?, ?, ?, ?, 'BME280')", (timestamp, temperature, humidity, pressure))
    conn.commit()

# Main loop to continuously measure and store data
while True:
    try:
        timestamp = int(time.time())
        for sensor_name, sensor in SENSORS.items():
            res = sensor.read()
            if len(res) == 2:
                res.append(None)
            store_measurement(timestamp, *res, sensor_name)