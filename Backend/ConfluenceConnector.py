from PythonConfluenceAPI import ConfluenceAPI
import json
from pymongo import MongoClient
import requests

#connection to mongodb
client = MongoClient('localhost', 27017)

api = ConfluenceAPI('se.bastian.esch@gmail.com', 'qUj9+UMj7Q', 'https://ibsolution.atlassian.net/wiki')
new_pages = api.get_content(space_key='SAPTECH')
#id_content = api.get_content_by_id('117873296', expand = 'body.storage')
#id_child_content = api.get_content_children('2523167')

content_data = json.dumps(new_pages, indent=2)
getJson = json.loads(content_data)
print("Content pages:")

#print(content_data)

#print(getJson) #whole values
# print(getJson['id']) #if only one key for each value exists

content_list = []
#gets every ID under a speciefied space
for i in getJson['results']:
    print('ID: ' + i['id'])
    id_content = api.get_content_by_id(i['id'], expand = 'body.storage')
    id_content = json.dumps(id_content, indent=2)
    print(id_content)
    #content_list.append(json.dumps(id_content, indent = 4))

#print(content_list)
# with open('data.json', 'w') as f:
#     json.dump(content_list, f, indent = 4)


