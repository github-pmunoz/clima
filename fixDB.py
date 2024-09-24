import sqlite3
import sys

# Connect to the database
conn = sqlite3.connect(sys.argv[1])
cursor = conn.cursor()

# Add two columns to the existing table
cursor.execute("ALTER TABLE measurements ADD COLUMN pressure REAL")
cursor.execute("ALTER TABLE measurements ADD COLUMN sensor TEXT")

# Update all existing rows with None values
cursor.execute("UPDATE measurements SET column1 = NULL, column2 = DHT11")

# Commit the changes and close the connection
conn.commit()
conn.close()