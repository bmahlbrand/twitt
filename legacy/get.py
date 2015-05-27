#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
from datetime import datetime

DATABASE="DB/twittr.db"
IMAGEPATH="IMAGES"
#############################################################
# Define main user page

def display(username, session):
   #Check session
   # if (session.check_session(form) != "passed"):
   #   login_form()
   #  return
   #add_tweet(username,session)
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	t = (username,)
   #get list of subscribed tweets
	c.execute('SELECT subscribed_user FROM subscriptions WHERE user=?' , t)
	s = c.fetchall()
	
	if len(s) == 0:
		sql = 'SELECT * FROM tweets WHERE owner="'+username+'" ORDER BY timestamp DESC'
		for row in c.execute(sql):  
			html="""
			<tr>
			<td>{name} </td><td>{time}</td><td><a href="login.cgi?action=remove&username={u}&session={s}&id={id}">Delete Tweet:{id}</a></td>
			</tr><tr><td>
			{text}
			
			</td>
			</tr>
			"""
			print(html.format(name=row[0],text=row[2],time=row[3], id=row[1], u=username, s=session))
	else:
		sql = 'SELECT * FROM tweets WHERE owner="'+username+'" OR owner IN (%s) ORDER BY  timestamp DESC' % ',  '.join('?' for a in s[0]) 
		for row in c.execute(sql,s[0]):  
			if (row[0] == username):
				html="""
				<tr>
				<td>{name} </td><td>{time}</td><td><a href="login.cgi?action=remove&username={u}&session={s}&id={id}">Delete Tweet:{id}</a></td>
				</tr><tr><td>
				{text}
			
				</td>
				</tr>
				"""
			else:
				html="""
				<tr>
				<td>{name} </td><td>{time}</td>
				</tr><tr><td>
				{text}
			
				</td>
				</tr>
				"""
			print(html.format(name=row[0],text=row[2],time=row[3], id=row[1], u=username, s=session))
    #Also set a session number in a hidden field so the
    #cgi can check that the user has been authenticated
       #print_html_content_type()

       #print(html.format(name=row[0]))
	conn.close();

##############################################################
# Define main function.
def main():
	form = cgi.FieldStorage()
	if "action" in form:
		action=form["action"].value
		username=form["username"].value
		session=form["session"].value
		if (action == "remove"):
			id=form["id"].value
			remove(username,session,id)
		else:
			display(username, session)
   # else:
    #    print("<H3><font color=\"red\">Incorrect user/password</font></H3>")

###############################################################
# Call main function.
main()