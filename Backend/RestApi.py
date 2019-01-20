from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'projectdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/projectdb'

mongo = PyMongo(app)

#------User methods-----#
#lists all users and returns their names
@app.route('/users', methods=['GET'])
def get_all_users():
  users = mongo.db.users
  output = []
  for u in users.find():
    output.append({'name' : u['name']})
  return jsonify({'result' : output})


#------Confluence data methods-----#
#lists all users and returns their names
@app.route('/confluencedata', methods=['GET'])
def get_all_confluencedata():
  confluencedata = mongo.db.confluencedata
  output = []
  for u in confluencedata.find():
    output.append({'documentId' : u['documentId'], 'title' : u['title'], 'date' : u['date'], 'body' : u['body'], 'tags' : u['tags']})
  return jsonify({'result' : output})


#@ID: searches database and returns only matching data
@app.route('/confluencedata/<Id>', methods=['GET'])
def get_document_by_Id(Id):
  confluencedata = mongo.db.confluencedata
  s = confluencedata.find_one({'documentId' : Id})
  if s:
    output = {'documentId' : s['documentId'], 'title' : s['title'], 'date' : s['date'], 'body' : s['body'], 'tags' : s['tags']}
  else:
    output = "No document with ID: " + Id + " found."
  return jsonify({'result' : output})

#if-else clause searches and returns only matching data
# @app.route('/confluencedata', methods=['GET'])
# def get_one_star(name):
#   # confluencedata = mongo.db.confluencedata
#   # s = confluencedata.find_one({'name' : name})
#   # if s:
#   #   output = {'name' : s['name'], 'distance' : s['distance']}
#   # else:
#   #   output = "No such name"
#   return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
