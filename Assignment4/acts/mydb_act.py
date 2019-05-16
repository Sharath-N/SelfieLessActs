from flask import Flask
import sqlite3 as sql

app = Flask(__name__)

conn = sql.connect('acts.db')
conn.execute('DROP TABLE acts_data')
conn.execute('CREATE TABLE acts_data (act_id BIGINT AUTO_INCREMENT,username TEXT,time_stamp TEXT,act_name TEXT,categoryname TEXT,upvote INT,imgB64 TEXT)')
print("Table created")

conn.close()
'''
with sql.connect('acts.db') as con:
	cur = con.cursor()
	cur.execute("INSERT INTO acts_data(act_id,username,time_stamp,act_name,upvote,categoryname,imgB64) VALUES (?,?,?,?,?,?,?)",(1,'Rohit','18-02-2019:10-24-43','caption1','blind',0,'base641'))
	cur.execute("INSERT INTO acts_data(act_id,username,time_stamp,act_name,categoryname,upvote,imgB64) VALUES (?,?,?,?,?,?,?)",(2,'Varun','19-02-2019:12-12-32','caption2','helping',0,'base642'))
	cur.execute("INSERT INTO acts_data(act_id,username,time_stamp,act_name,upvote,categoryname,imgB64) VALUES (?,?,?,?,?,?,?)",(3,'Varun','13-02-2019:12-12-32','caption2','helping',0,'base643'))
	cur.execute("INSERT INTO acts_data(act_id,username,time_stamp,act_name,upvote,categoryname,imgB64) VALUES (?,?,?,?,?,?,?)",(4,'Varun','11-02-2019:12-12-32','caption2','helping',0,'base644'))
	cur.execute("SELECT * FROM acts_data")
	cur.execute("SELECT * FROM acts_data ORDER BY time_stamp DESC")
	print(cur.fetchall())
	con.commit()
	
print("record created")
'''
