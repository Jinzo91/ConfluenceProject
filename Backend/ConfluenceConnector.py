from PythonConfluenceAPI import ConfluenceAPI
import json

def check_Connection(username, password, url):
    api = ConfluenceAPI(username, password, url)
    if api.get_spaces():
        return True
    else:
        return False

#required parameters: username, passsword, url
#optional: Confluence spaceKey, default is 'SAPTECH'
def get_content(username, password, url, spaceKey='SAPTECH'):
    # username = 'se.bastian.esch@gmail.com'
    # password = 'qUj9+UMj7Q'
    # url = 'https://ibsolution.atlassian.net/wiki'
    api = ConfluenceAPI(username, password, url)
    #gets the content based on the content type page and a space key (default=SAPTECH).
    #Set limit: Confluence server sided response has max-limit of 100 results per request, higher is not possible and default is 25.
    #Needs pagination and for-loops to get more results.
    new_pages = api.get_content(expand=('body.storage,history,metadata.labels'), space_key=spaceKey, content_type='page', limit=100)

    content_data = json.dumps(new_pages, indent=2)#careful: do not json.dump twice
    getJson = json.loads(content_data)
    #print(content_data)
    print("Loading Confluence data...")

    return getJson