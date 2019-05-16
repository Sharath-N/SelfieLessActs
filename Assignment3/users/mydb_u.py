from flask import Flask
import sqlite3 as sql

app = Flask(__name__)

conn = sql.connect('users.db')
#conn.execute('DROP TABLE users_data')
conn.execute('CREATE TABLE users_data (username TEXT,password TEXT)')
print("Table created")

conn.close()

'''
with sql.connect('users.db') as con:
	cur = con.cursor()
	cur.execute('INSERT INTO users_data VALUES (?,?)',('Rohit B','asddq',))
	con.commit()
	
print("record created")
'''
