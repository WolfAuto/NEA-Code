import sqlite3 as sql # python libary module for creating databases
db = sql.connect("updatedfile.db") # creates a connection to db file
cursor = db.cursor() # creates a cursor to interact with the file
cursor1 = db.cursor() # creates a second cursor to interact with the database
