from PythonConfluenceAPI import ConfluenceAPI
import json
from textblob import TextBlob

def tag_text(document):
    text = TextBlob(document)
    taggedText = text.tags
    return taggedText

def get_content():
    api = ConfluenceAPI('se.bastian.esch@gmail.com', 'qUj9+UMj7Q', 'https://ibsolution.atlassian.net/wiki')
    new_pages = api.get_content(expand=('body.storage,history,metadata.labels'))#grabs all content if no parameters specified
    #id_content = api.get_content_by_id('117873296', expand = 'body.storage')
    #id_child_content = api.get_content_children('2523167')
    content_data = json.dumps(new_pages, indent=2)#careful: do not json.dump twice
    getJson = json.loads(content_data)
    #print(content_data)
    print("Loading Confluence data...")

    #Testing code
    tags = []
    labels = []
    for i in getJson['results']:
        for j in i['metadata']['labels']['results']:
            tags.append(j['label'])
        labels.append(tags)
        tags = []
    #print(labels)
    return getJson

#get_content()
