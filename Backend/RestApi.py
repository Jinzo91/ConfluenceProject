from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from string import  punctuation
from Backend.Algorithm import generateTags
from Backend.Algorithm import get_tokens
from Backend.ConfluenceConnector import get_content
from Backend.ConfluenceConnector import check_Connection
from Backend.ConfluenceConnector import uploadTo_confluence

#install neccessary packages (including package _future_)
#Initiliazes the rest API as a flask app
app = Flask(__name__)
#Allows cross domain data transfer (required for data transfer between localhosts)
CORS(app)
#Check whether you have a database named projectdb, if not then create one.
app.config['MONGO_DBNAME'] = 'projectdb'
#Default MongoDB URI to connect to DB looks like this:
app.config['MONGO_URI'] = 'mongodb://localhost:27017/projectdb'
mongo = PyMongo(app)

#global variables for authentication purposes.
globalUser = ''
password = ''
url = ''
space = None
#After server is started it will show this message.
@app.route('/')
def hello_server():
    return 'Server is up and running.'


#------User Methods-----#

#@Deprecated
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


#Input: url, space key, username, password
#Output: username
#Registration: when a new user tries to login.
#Login: authenticates the user.
#Saves credentials to connect to Confluence.
@app.route('/api/user/login', methods=['POST'])
def login_user():
    users = mongo.db.users
    global url
    url = request.values['url']
    global space
    if 'space' in request.values:
        print('space key found')
        space = request.values['space']
    else:
        space = None
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
        #api = ConfluenceAPI(globalUser, password, url)
        if check_Connection:
            output = {'name' : user['name']}
            return jsonify({'name' : output})
    else:
        return False



#------Confluence Methods-----#

#Input: document ID
#Output: generated tags
#Lists all documents from the DB related to logged in user.
@app.route('/api/confluencedata', methods=['GET', 'POST'])
def get_all_confluenceData():
    confluencedata = mongo.db.confluencedata
    output = []
    for u in confluencedata.find({'name': globalUser}):
        output.append({'documentId' : u['documentId'], 'title' : u['title'], 'date' : u['date'], 'body' : u['body'], 'tags' : u['tags']})
    return jsonify({'result' : output}) #every return has HTTP status code


#Input: document ID
#Output: document
#Searches database and returns only matching ID and document
@app.route('/api/confluencedata/search/<Id>', methods=['GET'])
def get_document_by_Id(Id):
    confluencedata = mongo.db.confluencedata
    s = confluencedata.find_one({'documentId' : Id})
    if s:
        output = {'documentId': s['documentId'], 'title': s['title'], 'date': s['date'], 'body': s['body'], 'tags': s['tags']}
    else:
        output = "No document with ID: " + Id + " found."
    return jsonify({'result' : output})


#Input: username, pasword, url, space
#Output: downloaded docuements
#Downloads data through Confluence API using the given login parameters and saves everything (data is binded to a user).
@app.route('/api/confluencedata/download', methods=['GET'])
def download_confluenceData():
    confluenceData = mongo.db.confluencedata
    if space != None:
        documents = get_content(globalUser, password, url, space)
    else:
        documents = get_content(globalUser, password, url)
    #Mapping of json values from Confluence documents. Extracted json structure has to be the same as database structure.
    for doc in documents:
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
        confluenceData.update_one({'documentId': documentId},
                                  {'$set': {'documentId': documentId, 'title': title, 'date': date, 'body': body, 'tags': stringLabels, 'name': 'se.bastian.esch@gmail.com'}}, upsert=True)
    return jsonify(documents)



#------Tagging Methods-----#

#Input: document ID
#Output: generated tags
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
        output = tagged_text
    else:
        output = "No document with ID: " + id + " was found."
    return jsonify({'tags' : output})


#Input: document ID, original tags, newly generated tags
#Output: filtered tags which are saved to the DB
#Adds filtered new tags saved to the DB after comparing if certain tags already exists or not.
@app.route('/api/confluencedata/save/tag', methods=['POST'])
def save_tag():
    confluencedata = mongo.db.confluencedata
    id = request.values['docId']
    originalTags = request.values['originalTags']
    newTags = request.values['newTags']
    newTags = ' '.join(word.strip(punctuation) for word in newTags.split()
                    if word.strip(punctuation))
    s = confluencedata.find_one({'documentId': id})
    originalTagsToken = get_tokens(originalTags)
    newTagsToken = get_tokens(newTags)
    print(newTagsToken)
    if s:
        newUniqueTags = [w for w in newTagsToken if not w in originalTagsToken]
        print(newUniqueTags)
        original_tags = ''.join(s['tags'])
        print(original_tags)
        if len(newUniqueTags) > 1:
            newUniqueTagsString = ', '.join(newUniqueTags)
            if len(original_tags) >= 1:
                complete_tags = original_tags + ', ' + newUniqueTagsString
                confluencedata.update_one({'documentId': id}, {'$set': {'tags': complete_tags}})
                #uploadTo_confluence(complete_tags, id, globalUser, password, url)
                output = complete_tags
            else:
                complete_tags = newUniqueTagsString
                confluencedata.update_one({'documentId': id}, {'$set': {'tags': complete_tags}})
                output = complete_tags
        else:
            output = original_tags
    else:
        output = "Tags could not be saved for document with ID: " + id
    return jsonify({'tags': output})


if __name__ == '__main__':
    app.run(debug=True)
