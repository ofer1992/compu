# Trying to upload a file to moodle

import requests
import webbrowser

#Login to moodle
def login(user,pw):
    loginPage = "https://moodle2.cs.huji.ac.il/nu16/login/index.php"
    session = requests.session()
    res = session.post(loginPage, {"username": user, "password":
pw})
    return session, res

def page(res):
    open('temp.htm','w').write(res.text)
    webbrowser.open('temp.htm')

def get_sesskey(res):
    i = res.text.find("sess")
    if i == -1: return "FAIL"
    return res.text[i+10:i+20]

def upload(f,sess, key):
    url = "https://moodle2.cs.huji.ac.il/nu16/repository/filepicker.php?ctx_id=446183&itemid=517031988&env=filemanager&course=80428&maxbytes=10485760&areamaxbytes=-1&maxfiles=1&subdirs=1&sesskey="+key+"&action=browse&draftpath=%2F&savepath=%2F&repo_id=4"

    sess.get("https://moodle2.cs.huji.ac.il/nu16/repository/draftfiles_manager.php?ctx_id=446183&itemid=517031988&env=filemanager&course=80428&maxbytes=10485760&areamaxbytes=-1&maxfiles=1&subdirs=1&sesskey="+key+"&action=deletedraft&draftpath=%2F&filename=infi8.pdf")
    res = sess.post(url,files={'repo_upload_file': f})
    
    forms = {'lastmodified': '1496337956',
            'id': '220795',
            'userid': '442422',
            'action': 'savesubmission',
            'sesskey': key,
            '_qf__mod_assign_submission_form': '1',
            'files_filemanager': '517031988',
            'submitbutton': 'Save+changes'}

    page(sess.post("https://moodle2.cs.huji.ac.il/nu16/mod/assign/view.php", forms))
    return res

