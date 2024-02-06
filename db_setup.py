import sqlite3
import csv

conn = sqlite3.connect('mqtt_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS mqtt_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        soil_humidity REAL,
        soil_temperature REAL,
        n REAL,
        p REAL,
        k REAL,
        timestamp TIMESTAMP
    )
''')

conn.commit()
conn.close()