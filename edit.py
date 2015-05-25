#!/usr/bin/python

import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session

DATABASE="DB/twittr.db"
IMAGEPATH="images"
###############################
# display main
def options(username,session):

	html="""
	<HTML>
	<HEAD>
	<TITLE>PeteTwitt User Options</TITLE>
	</HEAD>

	<BODY BGCOLOR = white>
	
	<center><img src="../PeteTwitt2.png"><H2>Welcome to PeteTwitt! User Options</H2>
<br>
	 <a href="edit.cgi?action=change_pass&username={u}&session={s}">Change Password</a><br>
	<br>
	
	 <a href="edit.cgi?action=add_sub&username={u}&session={s}">Add Subscriber</a><br>
	<FORM ACTION="edit.cgi" METHOD="POST" enctype="multipart/form-data">
	Search for user to add:<INPUT TYPE=text NAME="subscriber">
	<input type="hidden" name="username" value="{u}">
	<input type="hidden" name="session" value="{s}">
	<input type="hidden" name="action" value="add_sub">
	<br>
	<input type="submit" value="Search">
	</form>

	<br>
	 <a href="edit.cgi?action=rem_sub&username={u}&session={s}">Remove Subscriber</a><br><br><br>
	
	<a href="login.cgi?action=refresh&username={u}&session={s}">Back to main</a>
	</center>
	</BODY>
	</HTML>
	"""
	
	print_html_content_type()
	print(html.format(u=username,s=session))

###########################
# edit password
def change_pass(username,session):

	html="""
	<HTML>
	
	<center><img src=../PeteTwitt2.png><H2>Change your PeteTwitt Password</H2>
	<FORM ACTION="edit.cgi" METHOD="POST" enctype="multipart/form-data">
	Enter New Password:<INPUT TYPE=text NAME="password2"><br>
	<input type="hidden" name="username" value="{u}">
	<input type="hidden" name="session" value="{s}">
	<input type="hidden" name="action" value="change">
	<br>
	<input type="submit" value="Change">
	</form>
	</HTML>
	"""
	print_html_content_type()
	print(html.format(u=username,s=session))
	
###########################
# edit password
def rem_sub(username,session):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()

	t = (username,)
	
	html="""
	<HTML>
	<center><img src=../PeteTwitt2.png><H2>Remove Subscriber</H2><br>
	Current Subscriptions:<br>
	"""
	print_html_content_type()
	print(html)
	
	for row in c.execute('SELECT subscribed_user FROM subscriptions WHERE user=?', t):

		html="""
		<a href="edit.cgi?action=remove&username={u}&subscriber={s}&session={ss}">Remove {s}</a>
		<br>
		"""
		print(html.format(u=username,s=row[0],ss=session))

	html="""
	<br><br>
	<a href="edit.cgi?action=refresh&username={u}&session={s}">Back to user options</a>
	</HTML>
	"""
	print(html.format(u=username,s=session))
	conn.close();
		
###########################
# edit password
def add_sub(username,session):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()

	t = (username,)
	
	html="""
	<HTML>
	<center><img src=../PeteTwitt2.png><H2>Add Subscriber</H2><br><br>
	"""
	print_html_content_type()
	print(html)
	
	for row in c.execute('SELECT email FROM users WHERE email!=?', t):

		html="""
		<a href="edit.cgi?action=add&username={u}&subscriber={s}&session={ss}">Add {s}</a>
		<br>
		"""
		print(html.format(u=username,s=row[0],ss=session))

	html="""<br><br>
	<a href="edit.cgi?action=refresh&username={u}&session={s}">Back to user options</a>
	</HTML>
	"""
	print(html.format(u=username,s=session))
	conn.close();	

# edit password
def add_sub2(username,session,subscriber):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()

	t = (username,"%%"+subscriber+"%%")
	
	html="""
	<HTML>
	<center><img src=../PeteTwitt2.png><H2>Found through Search</H2><br><br>
	"""
	print_html_content_type()
	print(html)
	sql = "SELECT email FROM users WHERE email!=? AND email LIKE ?"
	#a = '%' + t + '%'
	for row in c.execute('SELECT email FROM users WHERE email!=? AND email LIKE ?',t):

		html="""
		<a href="edit.cgi?action=add&username={u}&subscriber={s}&session={ss}">Add {s}</a>
		<br>
		"""
		print(html.format(u=username,s=row[0],ss=session))

	html="""<br><br>
	<a href="login.cgi?action=refresh&username={u}&session={s}">Back to main</a>
	</HTML>
	"""
	print(html.format(u=username,s=session))
	conn.close();
	
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
	
   ##############################################################
# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
		action=form["action"].value
		username=form["username"].value
		session=form["session"].value
		
		if (action == "change_pass"):
			change_pass(username,session)
		elif (action == "change"):
			password=form["password2"].value
			modify_pass(username,password)
			options(username, session)
		elif (action == "rem_sub"):
			rem_sub(username,session)
		elif (action == "remove"):
			sub = form["subscriber"].value
			remove(username,sub)
			rem_sub(username,session)
		elif (action == "add_sub"):
			if "subscriber" in form:
				sub = form["subscriber"].value
				add_sub2(username,session,sub)
			else:
				add_sub(username,session)
		elif (action == "add"):
			sub = form["subscriber"].value
			add(username,sub)
			add_sub(username,session)
		else:
			options(username, session)
   # else:
    #    print("<H3><font color=\"red\">Incorrect user/password</font></H3>")

###############################################################
# Call main function.
main()
