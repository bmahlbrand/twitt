import login

#upload picture
#######################################################

def upload_pic_data(form):
    #Check session is correct
    if (session.check_session(form) != "passed"):
        login_form()
        return

    #Get file info
    fileInfo = form['file']

    #Get user
    user=form["user"].value
    s=form["session"].value

    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)
        open(IMAGEPATH+'/user1/test.jpg', 'wb').write(fileInfo.file.read())
        image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
        print_html_content_type()
	print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
        print('<image src="'+image_url+'">')
    else:
        message = 'No file was uploaded'

###########################
# edit password
def modify_pass(username,password):

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (password, username)
    c.execute('UPDATE USERS set password=? WHERE email=?', t)
    conn.commit()
    conn.close();
    
    
###########################
# add subscriber
def add(username,subscriber):

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (username, subscriber)
    c.execute('INSERT INTO subscriptions VALUES (?, ?)', t)
    conn.commit()
    conn.close();

###########################
# remove subscriber
def remove(username,subscriber):
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (username, subscriber)
    c.execute('DELETE FROM subscriptions WHERE user=? AND subscribed_user=?', t)
    conn.commit()
    conn.close();
    
def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")
