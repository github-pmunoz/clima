import sys
import sqlite3

# Get the filename argument from the shell
filename = sys.argv[1]

# Connect to the database
conn = sqlite3.connect(filename)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store weather data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        humidity REAL
    )
''')

# Query the database
cursor.execute('SELECT * FROM weather')
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the cursor and the connection
cursor.close()
conn.close()