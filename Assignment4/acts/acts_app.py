from flask import Flask,jsonify,request,make_response
#from flask_httpauth import HTTPBasicAuth
import sqlite3 as sql
import requests
#auth = HTTPBasicAuth()
import datetime
import base64
import binascii
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)

c = 0

#3
@app.route('/api/v1/categories',methods=['GET'])
def ret_categories():
	global c
	c = c + 1
	con = sql.connect("categories.db")
	con.row_factory = sql.Row
	
	cur = con.cursor()
	cur.execute("select categoryname,posts from category_data")
	
	rows = cur.fetchall()

	if(not(rows)):
		return jsonify(),204
	ret_cat = {}
	for i in rows:
		ret_cat[i['categoryname']] = i['posts']
	return jsonify(ret_cat),200

#4
@app.route('/api/v1/categories',methods=['POST'])
def add_category():
	global c
	c = c + 1
	if(not(request.json)):
		return jsonify(),400
	try:
		with sql.connect("categories.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM category_data WHERE categoryname=?",(request.json[0],))
			out1 = cur.fetchall()
			if(len(out1)):
				return jsonify(),400
			cur.execute("INSERT INTO category_data (categoryname,username,posts) VALUES (?,?,?)",(request.json[0],'Rohit B',0))
			con.commit()
			return jsonify(),201
	except:
		con.rollback()
		return jsonify(),400
		
	
#5
@app.route('/api/v1/categories/<categoryName>',methods=['DELETE'])
def remove_category(categoryName):
	global c
	c = c + 1
	with sql.connect("categories.db") as con:
		cur = con.cursor()
		cur.execute("SELECT categoryname FROM category_data WHERE categoryname=?",(categoryName,))
		cat_name = cur.fetchall()
		if(not(cat_name)):
			return jsonify(),400
		cur.execute("DELETE FROM category_data WHERE categoryname=?",(categoryName,))
		con.commit()
		return jsonify(),200

#6 or #8
@app.route('/api/v1/categories/<categoryName>/acts',methods=['GET'])
def list_of_acts(categoryName):
	global c
	c = c + 1
	if(request.args.get('start')==None):
		return acts_of_category(categoryName)
	else:
		return list_acts_in_range(categoryName,request.args.get('start'),request.args.get('end'))

def acts_of_category(categoryName):
	global c
	c = c + 1
	with sql.connect("categories.db") as con:
		cur = con.cursor()
		cur.execute("SELECT categoryname FROM category_data WHERE categoryname=?",(categoryName,))
		cat_name = cur.fetchall()
		if(not(cat_name)):
			return jsonify(),400
			
	with sql.connect("acts.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM acts_data")
		total = cur.fetchall()
		if(len(total)>100):
			return jsonify(),413
		
		cur.execute("SELECT * FROM acts_data WHERE categoryname=?",(categoryName,))
		acts = cur.fetchall()
		
		if(not(acts)):
			return jsonify(),204
		out = []
		for i in range(len(acts)):
			ret_acts = {
				'act_id': acts[i][0],
				'username': acts[i][1],
				'time_stamp': acts[i][2],
				'caption': acts[i][3],
				'category name': acts[i][4],
				'upvotes': acts[i][5],
				'imgB64': acts[i][6]
			}
			out.append(ret_acts)
		return jsonify(out),200
		
def list_acts_in_range(categoryName,startRange,endRange):
	global c
	c = c + 1
	with sql.connect("categories.db") as con:
		cur = con.cursor()
		cur.execute("SELECT categoryname FROM category_data WHERE categoryname=?",(categoryName,))
		out = cur.fetchall()
		if(len(out)==0):
			return jsonify(),400
			
	with sql.connect("acts.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM acts_data WHERE categoryname=? ORDER BY time_stamp DESC",(categoryName,))
		acts = cur.fetchall()
		
		try:
			new_acts = acts[int(startRange)-1:int(endRange)]
		except:
			return jsonify(),413
		if(len(new_acts)>100):
			return jsonify(),413
		if(len(new_acts)==0):
			return jsonify(),204
		out = []
		for i in range(len(new_acts)):
			ret_acts = {
				'act_id': new_acts[i][0],
				'username': new_acts[i][1],
				'time_stamp': new_acts[i][2],
				'caption': new_acts[i][3],
				'category name': new_acts[i][4],
				'upvotes': new_acts[i][5],
				'imgB64': new_acts[i][6]
			}
			out.append(ret_acts)
		return jsonify(out),200
	
#7
@app.route('/api/v1/categories/<categoryName>/acts/size',methods=['GET'])
def size_of_category(categoryName):
	global c
	c = c + 1
	with sql.connect("categories.db") as con:
		cur = con.cursor()
		cur.execute("SELECT categoryname,posts FROM category_data WHERE categoryname=?",(categoryName,))
		out = cur.fetchall()
		if(len(out)==0):
			return jsonify(),400
		return jsonify([out[0][1]]),200
		'''
		if(out[0][1]):
			return jsonify([out[0][1]]),200
		else:
			return jsonify([out[0][1]]),204
		'''

#9
@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote():
	global c
	c = c + 1
	if(not(request.json)):
		return jsonify(),400
	with sql.connect("acts.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM acts_data WHERE act_id=?",(request.json[0],))
		out = cur.fetchall()
		if(len(out)==0):
			return jsonify(),400
		
		cur.execute("UPDATE acts_data SET upvote=upvote+1 WHERE act_id=?",(request.json[0],))
		
		con.commit()
		return jsonify(),200
		
#10
@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_act(actId):
	global c
	c = c + 1
	with sql.connect("acts.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM acts_data WHERE act_id=?",(actId,))
		out = cur.fetchall()
		if(len(out)==0):
			return jsonify(),400
		cur.execute("DELETE FROM acts_data WHERE act_id=?",(actId,))
		con.commit()
		return jsonify(),200
		
#11
@app.route('/api/v1/acts',methods=['POST'])
def upload_act():
	global c
	c = c + 1
	if(not(request.json)):
		return jsonify(),400
	a_id = request.json['actId']
	user = request.json['username']
	ts = request.json['timestamp']
	cap = request.json['caption']
	cat_name = request.json['categoryName']
	ib6 = request.json['imgB64']
	with sql.connect("categories.db") as con:
		cur = con.cursor()
		cur.execute("SELECT categoryname FROM category_data WHERE categoryname=?",(cat_name,))
		out = cur.fetchall()
		if(len(out)==0):
			return jsonify(),400
			
	with sql.connect("acts.db") as con:
		cur = con.cursor()
		cur.execute("SELECT act_id FROM acts_data WHERE act_id=?",(a_id,))
		out = cur.fetchall()
		if(len(out)):
			return jsonify(),400
		try:
			datetime.datetime.strptime(ts,'%d-%m-%Y:%S-%M-%H')
		except:
			return jsonify(),400
		#3
		req = requests.get("http://0.0.0.0:8080/api/v1/users")
		prev_user = req.json()
		if(user not in prev_user):
			return jsonify(prev_user),400
				
		#5
		if('upvote' in request.json):
			return jsonify(),400
		
		
		cur.execute("INSERT INTO acts_data VALUES (?,?,?,?,?,?,?)",(a_id,user,ts,cap,cat_name,0,ib6,))
		con.commit()
		with sql.connect("categories.db") as con1:
			cur1 = con1.cursor()
			cur1.execute("UPDATE category_data SET posts=posts+1 WHERE categoryname=?",(cat_name,))
			con1.commit()
		return jsonify(),201


# Get total number of acts
@app.route('/api/v1/count',methods=['GET'])
def acts_count():
	with sql.connect("acts.db") as con:
		cur = con.cursor()
		cur.execute("SELECT COUNT(act_id) FROM acts_data")
		tot_acts = cur.fetchall()
		return jsonify(tot_acts[0]),200


# Get total HTTP requests made to microservice
@app.route('/api/v1/_count',methods=['GET'])
def req_count():
	global c
	c = c + 1
	count = []
	count.append(c)
	return jsonify(count),200

# Reset HTTP requests counter
@app.route('/api/v1/_count',methods=['DELETE'])
def reset_count():
	global c
	c = 0
	return jsonify(),200

	
@app.errorhandler(405)
def method_not_found(e):
	return jsonify(),405
'''
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)	
   ''' 
if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=8000)#,port=1000) 
