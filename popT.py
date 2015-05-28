#!/usr/bin/python

import sqlite3
import datetime
from werkzeug import generate_password_hash

current_time = datetime.datetime.now().time()

def populate():
	print
	print ("Run only once or you will get error for duplicates")
	print 
	init_db()
	conn = sqlite3.connect('DB/twittr.db')
	c = conn.cursor()

	users = [('george@gmail.com', generate_password_hash('abc123'),'George','Constanza', '', 1),
	             ('mary@gmail.com',generate_password_hash('mary123'), 'Mary', 'Lamb',  '', 1),
	             ('peter@gmail.com',generate_password_hash('peter123'),'Peter','Piper', '', 1),
	            ]
	c.executemany('INSERT INTO users VALUES (?,?,?,?,?,?)', users)

	tweets = [(0, 'george@gmail.com',"tweet0",str(current_time),"NULL"),
	           (1, 'george@gmail.com',"tweet1",str(current_time),"NULL"),
	           (2, 'george@gmail.com',"tweet2",str(current_time),"NULL"),
	           (3, 'mary@gmail.com',"tweet3",str(current_time), "NULL"),]      
	c.executemany('INSERT INTO tweets  VALUES (?,?,?,?,?)', tweets)

	subs = [
	    ('george@gmail.com', 'mary@gmail.com'),
	    ('george@gmail.com', 'peter@gmail.com'),
	    ('mary@gmail.com', 'peter@gmail.com'), ]

	c.executemany('INSERT INTO subscriptions VALUES (?,?)', subs)


	# commit or there are no changes
	conn.commit()

	print ('Done.')


if __name__ == '__main__':
	populate()