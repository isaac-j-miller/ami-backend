import sqlite3 as sql
with open('database_location.txt', 'r') as f:
    database_path = f.read()

sql.connect(database_path)