from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from Backend.ConfluenceConnector import get_content
from PythonConfluenceAPI import ConfluenceAPI
from Backend.Algorithm import generateTags


#install neccessary packages + the package _future_
#Initiliazes the rest API as a flask app
app = Flask(__name__)
#Allows cross domain data transfer (required for data transfer between localhosts)
CORS(app)
#Check whether you have a database named projectdb, if not then create one.
app.config['MONGO_DBNAME'] = 'projectdb'
#MongoDB URI to connect to DB looks like this:
app.config['MONGO_URI'] = 'mongodb://localhost:27017/projectdb'
mongo = PyMongo(app)

#global variables for authentication purposes.
globalUser = ''
password = ''
url =''

#After server is started it will show a message.
@app.route('/')
def hello_server():
    return 'Server is up and running.'

#------User Methods-----#

#Register: creates a new user, hashes the password and saves it to DB. Returns new user name as JSON.
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

#Login: authenticates the user.
#Saves credentials to connect to Confluence.
@app.route('/api/user/login', methods=['POST'])
def login_user():
    users = mongo.db.users
    req = request.values.to_dict()
    global url
    url = request.values['url']
    global space
    space = request.values['space']
    global globalUser
    globalUser = request.values['username']
    global password
    password = request.values['password']
    encryptedPassword = generate_password_hash(password)
    users.update_one({'name': globalUser},
                     {'$set': {'name': globalUser, 'password': encryptedPassword}}, upsert=True)
    user = users.find_one({'name': globalUser})
    hashedPassword = user['password'] #gets hashed password from DB
    if check_password_hash(hashedPassword, password): #validates encrypted password with input password
        api = ConfluenceAPI(globalUser, password, url)
        if api.get_spaces():
            output = {'name' : user['name']}
            return jsonify({'name' : output})
    else:
        return False



#------Confluence Methods-----#
#Lists all documents from the DB according to logged in user.
@app.route('/api/confluencedata', methods=['GET', 'POST'])
def get_all_confluenceData():
    confluencedata = mongo.db.confluencedata
    print(request.values)
    #requestName = request.values['username']
    output = []
    for u in confluencedata.find({'name': 'se.bastian.esch@gmail.com'}):
        output.append({'documentId' : u['documentId'], 'title' : u['title'], 'date' : u['date'], 'body' : u['body'], 'tags' : u['tags']})
    return jsonify({'result' : output}) #every return has HTTP status code


#Searches database and returns only matching ID and data
@app.route('/api/confluencedata/search/<Id>', methods=['GET'])
def get_document_by_Id(Id):
    confluencedata = mongo.db.confluencedata
    s = confluencedata.find_one({'documentId' : Id})
    if s:
        output = {'documentId': s['documentId'], 'title': s['title'], 'date': s['date'], 'body': s['body'], 'tags': s['tags']}
    else:
        output = "No document with ID: " + Id + " found."
    return jsonify({'result' : output})



#Downloads data from confluence API using the given login parameters
@app.route('/api/confluencedata/download', methods=['GET'])
def download_confluenceData():
    confluenceData = mongo.db.confluencedata
    documents = get_content(globalUser, password, url, space)
    #print(documents)
    #Mapping of json values from Confluence documents. Extracted json structure has to be the same as database structure.
    for doc in documents['results']:
        documentId = doc['id']
        title = doc['title']
        date = doc['history']['createdDate'][0:10]
        body = doc['body']['storage']['value']
        tags = ""
        labels =[]
        stringLabels = ''
        for i in doc['metadata']['labels']['results']:
            tags = i['label']
            labels.append(tags)
            stringLabels = ', '.join(labels)
            tags = ""
            #print(stringLabels)
        confluenceData.update_one({'documentId': documentId},
                                  {'$set': {'documentId': documentId, 'title': title, 'date': date, 'body': body, 'tags': stringLabels, 'name': globalUser}}, upsert=True)  # database structure

    return jsonify(documents)

#------Tagging Method-----#
#Uses the tag function in Algorithm.py to generate new labels for the document.
tagged_text =''
@app.route('/api/confluencedata/tag', methods=['POST'])
def tag_document():
    confluencedata = mongo.db.confluencedata
    id = request.values['docId']
    s = confluencedata.find_one({'documentId': id})
    if s:
        title = s['title']
        body = s['body']
        tagged_text = generateTags(title, body)
        output = {'tags': tagged_text}

    else:
        output = "No document with ID: " + id + " was found."
    return (output)


@app.route('/api/confluencedata/save/tag', methods=['GET'])
def save_tag():
    confluencedata = mongo.db.confluencedata
    id = request.values['docId']
    s = confluencedata.find_one({'documentId': id})
    if s:
        original_tags = ', '.join(s['tags'])
        complete_tags = original_tags.append(tagged_text)
        confluencedata.update_one({'documentId': id}, {'$set': complete_tags})
        output = complete_tags
    else:
        output = "Tags could not be saved for document with ID: " + id
    return (output)


if __name__ == '__main__':
    app.run(debug=True)
