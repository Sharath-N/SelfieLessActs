#flask database
from flask import Flask
import sqlite3 as sql

app = Flask(__name__)

conn = sql.connect('categories.db')
#conn.execute('DROP TABLE category_data')
conn.execute('CREATE TABLE category_data (cat_id BIGINT AUTO_INCREMENT,categoryname TEXT,username TEXT,posts INT)')
print("Table created")

conn.close()
'''
with sql.connect('categories.db') as con:
	cur = con.cursor()
	cur.execute("INSERT INTO category_data (cat_id,categoryname,username,posts) VALUES (?,?,?,?)",(1,'blind','Rohit',1))
	cur.execute("INSERT INTO category_data (cat_id,categoryname,username,posts) VALUES (?,?,?,?)",(2,'helping','Rohit B',3))
	con.commit()
	
print("record created")
'''
