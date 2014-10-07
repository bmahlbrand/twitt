#!/usr/bin/python

import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import cgi, string, sys, os, re, random

import urlparse

MYLOGIN="bahlbran"
DATABASE="/homes/"+MYLOGIN+"/shared_twitter/petetwitt.db"
IMAGEPATH="/homes/"+MYLOGIN+"/shared_twitter/images"
#import account_management
print("Content-Type: text/html\n\n")

def validate():
		
	html = """
<HTML>
<HEAD>
<TITLE>activate</TITLE>
</HEAD>
<BODY BGCOLOR = white>
<center><H2>validated</H2></center>
<p>Thanks for confirming, welcome to PeteTwitt!</p>
</BODY>
</HTML>
"""

	print(html)

def activate(email):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	t = (1, email)
	#get list of subscribed tweets
	c.execute('UPDATE USERS set activated=? WHERE email=?', t)
	conn.commit()
	#s = c.fetchall()
   
	#sql = 'SELECT * FROM tweets WHERE owner="'+username+'" OR owner IN (%s) ORDER BY  timestamp DESC' % ',  '.join('?' for a in s[0]) 

def main():
	form = cgi.FieldStorage()
	email = form["email"].value
	action=form["action"].value
	activate(email)
	validate()

main()