from flask import Flask,jsonify,request,make_response
#from flask_httpauth import HTTPBasicAuth
import sqlite3 as sql
#auth = HTTPBasicAuth()
import datetime
import base64
import binascii
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)
#1
@app.route('/api/v1/users',methods=["POST"])
def add_user():
	if(not(request.json)):
		return jsonify(),400
	with sql.connect('users.db') as con:
		cur = con.cursor()
		cur.execute('SELECT * FROM users_data where username=?',(request.json['username'],))
		out = cur.fetchall()
		if(len(out)):
			return jsonify(),400
		#checking sha1
		pwd = request.json['password']
		for i in pwd:
			if(ord(i)>102):
				return jsonify(),400
		
		cur.execute("INSERT INTO users_data VALUES (?,?)",(request.json['username'],pwd,))
		con.commit()
		return jsonify(),201
		
#2
@app.route('/api/v1/users/<userName>',methods=['DELETE'])
def remove_user(userName):
	with sql.connect('users.db') as con:
		cur = con.cursor()
		cur.execute('SELECT username FROM users_data where username=?',(userName,))
		out = cur.fetchall()
		if(not(len(out))):
			return jsonify(),400
		cur.execute("DELETE FROM users_data where username=?",(userName,))
		con.commit()
		return jsonify(),200

#3
@app.route('/api/v1/users',methods=['GET'])
def listallusers():
	con = sql.connect("users.db")
	
	cur = con.cursor()
	cur.execute("select username from users_data")
	
	rows = cur.fetchall()
	if(not(rows)):
		return jsonify(),204
	out = []
	for i in rows:
		out.append(i[0])
	return jsonify(out),200
	
@app.errorhandler(405)
def method_not_found(e):
	return jsonify(),405
'''
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)	
   ''' 
if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=80)
