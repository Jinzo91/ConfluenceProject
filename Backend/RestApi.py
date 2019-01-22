from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from Backend.ConfluenceConnector import get_content


app = Flask(__name__)
#Check whether you have a database named projectdb, if not then create one.
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


@app.route('/users', methods=['POST'])
def add_user():
    users = mongo.db.users
    name = request.json['name']
    password = request.json['password']
    new_user = users.insert({'name': name, 'password': password})
    u = users.find_one({'_id': new_user})
    output = {'name' : u['name']}
    return jsonify({'result' : output}) #returns a json object and HTTP status code (eg. 200: success, 400: failure etc.)

#------Confluence data methods-----#
#lists all users and returns their names
@app.route('/confluencedata', methods=['GET'])
def get_all_confluenceData():
    confluencedata = mongo.db.confluencedata
    output = []
    for u in confluencedata.find():
        output.append({'documentId' : u['documentId'], 'title' : u['title'], 'date' : u['date'], 'body' : u['body'], 'tags' : u['tags']})
    return jsonify({'result' : output}) #every return has HTTP status code


#@ID: searches database and returns only matching data
@app.route('/confluencedata/<Id>', methods=['GET'])
def get_document_by_Id(Id):
    confluencedata = mongo.db.confluencedata
    s = confluencedata.find_one({'documentId' : Id})
    if s:
        output = {'documentId': s['documentId'], 'title': s['title'], 'date': s['date'], 'body': s['body'], 'tags': s['tags']}
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


#downloads data from confluence API and saves it in the database
@app.route('/confluencedata/download', methods=['GET'])
def download_confluenceData():
    confluenceData = mongo.db.confluencedata
    documents = get_content()

    #Mapping of json values from Confluence documents. Extracted json structure has to be the same as database structure.
    for doc in documents['results']:
        documentId = doc['id']
        title = doc['title']
        date = doc['history']['createdDate'][0:10]
        body = doc['body']['storage']['value']
        tags = []
        labels =[]
        for i in doc['metadata']['labels']['results']:
            tags.append(i['label'])
            labels.append(tags)
            tags = []

        confluenceData.update({'documentId': documentId},
            {'documentId': documentId, 'title': title, 'date': date, 'body': body, 'tags': labels}, upsert=True)  # database structure

    return ('Download successfull.')

if __name__ == '__main__':
    app.run(debug=True)
