# Trying to upload a file to moodle

import requests
import bs4
import re



#Login to moodle
def login(user,pw):
    loginPage = "https://moodle2.cs.huji.ac.il/nu16/login/index.php"
    session = requests.session()
    res = session.post(loginPage, {"username": user, "password":
pw})
    return session

# Build confirm form submission
def confirm(tags,itemid):
    forms = {}
    for tag in tags:
        forms[tag.get('name')] = tag.get('value')
    forms['files_filemanager'] = itemid
    forms['submitbutton'] = 'Save+changes'
    return forms


# TODO: Add case where there is already a file present
# Receives session, id of upload page and file to be uploaded
def upload(s,id,f):
    res = s.get("https://moodle2.cs.huji.ac.il/nu16/mod/assign/view.php?id="+id+"&action=editsubmission") # edit submission page
    bs = bs4.BeautifulSoup(res.text)
    data = bs.select('noscript object')[0].get('data') # extracts the file manager
    data = data.replace('&amp;','&')
    
    # Here we extract data later to be used for the confirm upload POST
    tags = bs.select('form.mform > div input')
    m = re.search(r'itemid=(\d*)',data)
    itemid = m.group(1)
    forms = confirm(tags,itemid)
    
    # Here we get the enter the file submission page, extract the filepicker url and modify it to upload our file
    res = s.get(data)
    bs = bs4.BeautifulSoup(res.text)
    data = bs.select('div.filemanager-toolbar a')[0].get('href') # getting the upload url
    data = data.replace('&amp;','&')
    data = data.replace('action=plugins', 'action=upload')
    data += "&repo_id=4"
    s.post(data,files={'repo_upload_file': f})
    
    # Confirm upload POST
    s.post("https://moodle2.cs.huji.ac.il/nu16/mod/assign/view.php?", forms)
    
    
    
