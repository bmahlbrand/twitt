#!/usr/bin/python
import smtplib 
from email.mime.text import MIMEText

import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import cgi, string, sys, os, re, random

import session

DATABASE="DB/twittr.db"
IMAGEPATH="IMAGES"

#import account_management
print("Content-Type: text/html\n\n")

def create_new_session(user):
    return session.create_session(user)

def add_user_to_db(form):
	email = form["email"]
	password = form["password"]
	first_name = form["first_name"]
	last_name = form["last_name"]
	filepath = IMAGEPATH+"/"+email+"/"
    #profile_pic = form["profile_pic"]
	#profile_pic = form["upload_pic"].value

	#add email_exists
	if email_exists(email) == "passed":
		session=create_new_session(email)

		conn = sqlite3.connect(DATABASE)
		c = conn.cursor()
		t = [('+email+', '+first_name+', '+last_name+', '+password+', '+filepath+', 0)]
		c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (email, password, first_name, last_name, filepath, 0))
		conn.commit()
		conn.close();

		upload_pic_data(form)
		
		print("<H3><font color=\"blue\">Sucksess!!  Check your inbox and verify</font></H3>")
	#elif email_exists(email) == "failed":
		create_user_email(form)
	
def email_exists(email):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	t = (email,)
	c.execute('SELECT * FROM users WHERE email=?', t)

	row = email = c.fetchone()
	conn.close();

	if row == None:
		return "passed"
	elif row != None:
		print("<H3><font color=\"red\">user exists</font></H3>")
		return "failed"

def upload_pic_data(form):
    #Check session is correct
    #Get file info
	fileInfo = form['profile_pic']

    #Get user
	user = form["email"].value
	#s=form["session"].value
	filepath = IMAGEPATH+"/"+user+"/"
	
	if not os.path.exists(filepath):
		os.makedirs(filepath)
		
    # Check if the file was uploaded
	if fileInfo.filename:
        # Remove directory path to extract name only
		fileName = os.path.basename(fileInfo.filename)
		
		open(IMAGEPATH+'/' +user+ '/' + fileName, 'wb').write(fileInfo.file.read())
		image_url="create_user.cgi?action=show_image&user={user}".format(user=user)
		#print_html_content_type()
		print('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
		print('<image src="'+image_url+'">')
	else:
		print('No file was uploaded')

def show_image(form):
    #Check session
    if session.check_session(form) != "passed":
       login_form()
       return

    # Your code should get the user album and picture and verify that the image belongs to this
    # user and this album before loading it

    username=form["username"].value

    # Read image
    with open(IMAGEPATH+username+'/test.jpg', 'rb') as content_file:
       content = content_file.read()

    # Send header and image content
    hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
    print(hdr+content)

#email...
#add
def create_user_email(form):
	#print form["email"].VALUE
	#fp(registration_confirmation, 'rb')
	#msg = MIMEText(fp.read())
	me = "johncarmack@doom.com"
	email = form["email"].value
	
	body = """
To complete setting up your account, please click the following link to confirm your email is valid:
"http://data.cs.purdue.edu:8892/petetwitt/validate.cgi?action=activate&email={0}"
""".format(email)



	msg = MIMEText(body)
	#fp.close()

	msg['Subject'] = 'Validate your PeteTwitt account' #% registration_confirmation
	msg['From'] = me
	msg['To'] = email

	s = smtplib.SMTP('localhost')
	s.sendmail(me, [email], msg.as_string())
	s.quit()

def main():
	# create_user_form()
	form = cgi.FieldStorage()
	
	if "action" in form:
		action=form["action"].value
		if action == "create_user":
			if "email" in form and "password" in form and "first_name" in form and "last_name" in form and "profile_pic":
				add_user_to_db(form)
		elif action == "show_image":
			show_image(form)
			print("show image")
main()