#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
# import session
from datetime import datetime

#####
# TO DO
# make db changes
# encrypt passwords?
# display profile pic next to name in tweet
# make look pretty
#check for bugs
#####

DATABASE="DB/twittr.db"
IMAGEPATH="IMAGES"

def check_password(user, passwd):

	
	return check_password_hash(self.pwdhash, passwd)
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	t = (user,)
	c.execute('SELECT * FROM users WHERE email=?', t)

	row = stored_password = c.fetchone()

	conn.close()

	if row != None: 
		stored_password = row[1]
		print(stored_password)
		print(passwd)
		# valid = row[5]
		if (stored_password == passwd):
			# if (valid == 1):
				return 'passed'
		else:
			return 'badpasswd'
	else:
		return 'badusernm'

	return 'failed'

#################################################################
# def create_new_session(user):
# 	return session.create_session(user)

#############################################################
# Define main user page
def display_main_page(username, session):
	 #Check session
	 # if (session.check_session(form) != "passed"):
	 #   login_form()
	 #  return
	add_tweet(username,session)
	# conn = sqlite3.connect(DATABASE)
	# c = conn.cursor()
	# t = (username,)
	 #get list of subscribed tweets
	# c.execute('SELECT subscribed_user FROM subscriptions WHERE user=?' , t)

	# s = c.fetchall()
	 
 #  sql = 'SELECT * FROM tweets WHERE owner="'+username+'" OR owner IN (%s) ORDER BY  timestamp DESC' % ',  '.join('?' for a in s[0]) 
	 # get all own tweets and subcriber tweets sort by timestamp from tweets table
	 #
 
	# for row in c.execute(sql,s[0]):
	html="""<center>
	<TABLE>
	<div id="refreshDiv" style="width:1000px;background:white;border: 3px solid;border-color:yellow;"> </div>
		</TABLE></center>"""
		#Also set a session number in a hidden field so the
		#cgi can check that the user has been authenticated
			 #print_html_content_type()
		 #  print(html.format(name=row[0],text=row[2],time=row[3]))
	print(html)
			 #print(html.format(name=row[0]))
	 #conn.close();

##################################
# add tweet
def add_tweet(username,session):
 #<a href="get.cgi?action=refresh&username={u}&session={se}">Create new album</a>
	html="""
	<HTML>
	<HEAD>
	<link rel="stylesheet" type="text/css" href="style.css">
	<TITLE>PeteTwitt</TITLE>
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script>
	<script type="text/javascript">
	var refreshPage = setInterval(
	function ()	{{
	$('#refreshDiv').load('get.cgi?action=login&username={username}&session={session}');
	}}, 1000); // refresh every second
	</script>
	</HEAD>
	<BODY BGCOLOR = white>
	<center><img src="PeteTwitt2.png"><H2>PeteTwitt</H2>
	<H3>Post New Tweet</H3>
		<a href="edit.cgi?action=edit&username={username}&session={session}">Edit User Preferences</a>
	<TABLE BORDER = 0>
				<FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
				<input type="hidden" name="username" value="{username}">
				<input type="hidden" name="session" value="{session}">
				<input type="hidden" name="action" value="addtweet">

	<TR><TH>Tweet Text:</TH><TD><INPUT TYPE=text NAME="text" SIZE="140"></TD><TR>
	<TR><TH>Tweet Picture:</TH><TD><INPUT TYPE=FILE NAME="upload_pic"></TD></TR>
	</TABLE>
	<INPUT TYPE=submit VALUE="PeteTweet!">
	</FORM>
				</center>
	</BODY>
	</HTML>
	"""
	user=username
	s=session
	print_html_content_type()
	print(html.format(username=user,session=s))

def post_tweet(form):

	#Check session
 	# if session.check_session(form) != "passed":
	#    login_form()
	#   return

	text = form["text"].value
	current_time = datetime.now()
	
	#profile_pic = form["upload_pic"].value
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	username=form["username"].value
	t = (username,None,text,current_time.strftime('%Y/%m/%d %I:%M:%S'), "NULL")
	c.execute("INSERT INTO tweets VALUES (?,?, ?, ?, ?)", t )
	conn.commit()
	conn.close();



###########################
# remove tweet
def remove(username,session, tid):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	t = (username, tid)
	c.execute('DELETE FROM tweets WHERE owner=? AND tweet_id=?', t)
	conn.commit()
	conn.close(); 
	
##############################################################
# Define main function.
def main():
	form = cgi.FieldStorage()
	if "action" in form:
		action=form["action"].value
				#print("action=",action)
		if action == "login":
			if "username" in form and "password" in form:
								#Test password
				username=form["username"].value
				password=form["password"].value
								# add check for validated, if not validate print notvalidated, check email
				if check_password(username, password)=="passed":
					session=create_new_session(username)
									# display_admin_options(username, session)
									# diplay main user page
					display_main_page(username, session)
				else:
					login_form()
					print("<H3><font color=\"blue\">Incorrect user/password, Please Try Again</font></H3>")
		elif (action == "new-album"):
			new_album(form)
		elif (action == "upload"):
			upload(form)
		elif (action == "show_image"):
			show_image(form)
		elif action == "upload-pic-data":
			upload_pic_data(form)
		elif action == "addtweet":
			post_tweet(form)
			username = form["username"].value
			session = form["session"].value
			display_main_page(username, session)
		elif action == "refresh":
			username = form["username"].value
			session = form["session"].value
			display_main_page(username, session)
		elif action == "remove":
			username = form["username"].value
			session = form["session"].value
			id=form["id"].value
			remove(username,session,id)
			display_main_page(username, session)
	# 	else:
	# 		login_form()
	# else:
	# 	login_form()
		 
		 
##############################################################
## UNUSED
#############################################################

##########################################################
# Diplay the options of admin
def display_admin_options(user, session):
		html="""
				<H1> PeteTwitt User  Options</H1>
				<ul>
				<li> <a href="login.cgi?action=new-album&user={user}&session={session}">Create new album</a>
				<li> <a href="login.cgi?action=upload&user={user}&session={session}">Upload Picture</a>
				<li> <a href="login.cgi?action=show_image&user={user}&session={session}">Show Image</a>
				<li> Delete album
				<li> Make album public
				<li> <a href="login.cgi?action=change_password&user={user}&session={session}">Change Password</a>
				</ul>
				"""
				#Also set a session number in a hidden field so the
				#cgi can check that the user has been authenticated

		print_html_content_type()
		print(html.format(user=user,session=session))



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
		open(IMAGEPATH+'/' +user+ '/' +filename, 'wb').write(fileInfo.file.read())
		image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
		print_html_content_type()
		print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
		print('<image src="'+image_url+'">')
	else:
		message = 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")

###############################################################################

def upload(form):
	# if session.check_session(form) != "passed":
		 # login_form()
		 # return

	html="""
			<HTML>
			<FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
					<input type="hidden" name="user" value="{user}">
					<input type="hidden" name="session" value="{session}">
					<input type="hidden" name="action" value="upload-pic-data">
					<BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
					<br>
					<input type="submit" value="Press"> to upload the picture!
			</form>
			</HTML>
	"""

	user=form["user"].value
	s=form["session"].value
	print_html_content_type()
	print(html.format(user=user,session=s))


##############################################################
def new_album(form):
	#Check session
	if session.check_session(form) != "passed":
		 return

	html="""
			<H1> New Album</H1>
			"""
	print_html_content_type()
	print(html);

##############################################################
def show_image(form):
	#Check session
	# if session.check_session(form) != "passed":
		 # login_form()
		 # return

	# Your code should get the user album and picture and verify that the image belongs to this
	# user and this album before loading it

	#username=form["username"].value

	# Read image
	with open(IMAGEPATH+'/user1/test.jpg', 'rb') as content_file:
		 content = content_file.read()

	# Send header and image content
	hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
	print (hdr+content)

###############################################################
# Call main function.
main()
