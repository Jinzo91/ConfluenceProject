from PythonConfluenceAPI import ConfluenceAPI
from PythonConfluenceAPI import all_of
import json

#A function to authenticate/check if the login parameters are valid against a Confluence server
def check_Connection(username, password, url):
    api = ConfluenceAPI(username, password, url)
    if api.get_spaces():
        return True
    else:
        return False

#required parameters: username, passsword, url
#optional: Confluence spaceKey, default is 'SAPTECH'
def get_content(username, password, url, spaceKey='SAPTECH'):
    api = ConfluenceAPI(username, password, url)
    #gets the content based on the content type page and a space key (default=SAPTECH).
    #Set limit: Confluence has a server sided response limit of 100 results per request, higher is not possible.
    #Uses pagination and for-loops to get more results.

    new_pages = all_of(api.get_content, expand=('body.storage,history,metadata.labels'),
                       space_key=spaceKey, content_type='page', limit=300)
    print(type(new_pages))
    list_pages =[]
    for i in (new_pages):
        list_pages.append(i)
    content_data = json.dumps(list_pages, indent=2)#careful: do not json.dump twice
    getJson = json.loads(content_data)
    print("Loading Confluence data...")
    return getJson

#Uplaods labels/tags to Confluence
def uploadTo_confluence(tags, docId, username, password, url,):
    api = ConfluenceAPI(username, password, url)
    tagList = tags.split(', ')
    api.create_new_label_by_content_id(docId, tagList)