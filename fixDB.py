import sqlite3
import sys

# Connect to the database
conn = sqlite3.connect(sys.argv[1])
cursor = conn.cursor()

# Update all existing rows with None values
cursor.execute("UPDATE measurements SET pressure = NULL, sensor = DHT11")

# Commit the changes and close the connection
conn.commit()
conn.close()