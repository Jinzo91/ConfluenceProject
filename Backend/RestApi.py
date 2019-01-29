from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from Backend.ConfluenceConnector import get_content
from Backend.ConfluenceConnector import tag_text

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

#install neccessary packages + the package future
app = Flask(__name__)
CORS(app)
#Check whether you have a database named projectdb, if not then create one.
app.config['MONGO_DBNAME'] = 'projectdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/projectdb'

mongo = PyMongo(app)

@app.route('/')
def hello_server():
    return 'Server is up and running.'

#------User Methods-----#

#lists all users and returns their names
@app.route('/api/user/all', methods=['GET'])
def get_all_users():
    users = mongo.db.users
    output = []
    for u in users.find():
        output.append({'name' : u['name']})
    return jsonify({'result' : output})

#Register: creates a new user and saves it to DB. Returns new user name as JSON.
@app.route('/api/user/register', methods=['POST'])
def add_user():
    users = mongo.db.users
    name = ''
    password =''
    for key in request.form:
        name = key['name']
        password = key['password']

    encryptedPassword = generate_password_hash(password)
    new_user = users.insert({'name': name, 'password': encryptedPassword})
    u = users.find_one({'_id': new_user})
    output = {'name' : u['name']}
    return jsonify({'result' : output}) #returns a json object and the HTTP status code (eg. 200: success, 400: failure etc.)

#Login
@app.route('/api/user/login', methods=['POST'])
def login_user():
    users = mongo.db.users
    name = ''
    password = ''
    print(request.form)
    name = request.form['name']
    password = request.form['password']
    # for key in request.form:
    #     name = key['name']
    #     password = key['password']

    user = users.find_one({'name': name})
    hashedPassword = user['password'] #gets hashed password from DB
    if check_password_hash(hashedPassword, password): #validates encrypted password with input password
        output = {'name' : user['name']}
        return jsonify({'result' : output})
    else:
        return False



#------Confluence Data Methods-----#
#lists all users and returns their names
@app.route('/api/confluencedata', methods=['GET'])
def get_all_confluenceData():
    confluencedata = mongo.db.confluencedata
    output = []
    for u in confluencedata.find():
        output.append({'documentId' : u['documentId'], 'title' : u['title'], 'date' : u['date'], 'body' : u['body'], 'tags' : u['tags']})
    return jsonify({'result' : output}) #every return has HTTP status code


#Searches database and returns only matching ID and data
@app.route('/api/confluencedata/<Id>', methods=['GET'])
def get_document_by_Id(Id):
    confluencedata = mongo.db.confluencedata
    s = confluencedata.find_one({'documentId' : Id})
    if s:
        output = {'documentId': s['documentId'], 'title': s['title'], 'date': s['date'], 'body': s['body'], 'tags': s['tags']}
    else:
        output = "No document with ID: " + Id + " found."
    return jsonify({'result' : output})


#downloads data from confluence API and saves it in the database
@app.route('/api/confluencedata/download', methods=['GET'])
def download_confluenceData():
    confluenceData = mongo.db.confluencedata
    documents = get_content()

    #Mapping of json values from Confluence documents. Extracted json structure has to be the same as database structure.
    for doc in documents['results']:
        documentId = doc['id']
        title = doc['title']
        date = doc['history']['createdDate'][0:10]
        body = doc['body']['storage']['value']
        tags = ""
        labels =[]
        for i in doc['metadata']['labels']['results']:
            tags = i['label']
            labels.append(tags)
            tags = ""
        if labels:
            print(labels[0])
        confluenceData.update({'documentId': documentId},
            {'documentId': documentId, 'title': title, 'date': date, 'body': body, 'tags': labels}, upsert=True)  # database structure

    return ('Download successfull!')


#Uses the tag function in ConfluenceConnector.py to generate new labels for the document.
@app.route('/api/confluencedata/tag/<Id>', methods=['GET'])
def tag_document(Id):
    confluencedata = mongo.db.confluencedata
    s = confluencedata.find_one({'documentId' : Id})
    if s:
        output = {'documentId': s['documentId'], 'title': s['title'], 'body': s['body'], 'tags': s['tags']}
        tagged_text = tag_text(json.dumps(output, indent=2))
        #stopWords = set(stopwords.words("english"))
        #words = word_tokenize(json.dumps(output, indent=2))

    else:
        tagged_text = "No document with ID: " + Id + " found."
    return jsonify({'result' : tagged_text})

if __name__ == '__main__':
    app.run(debug=True)
