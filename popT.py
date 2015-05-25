#!/usr/bin/python

import sqlite3
import datetime
current_time = datetime.datetime.now().time()

def populate():
	print
	print ("Run only once or you will get error for duplicates")
	print 

	conn = sqlite3.connect('DB/twittr.db')
	c = conn.cursor()

	users = [('george@gmail.com', 'abc123','George','Constanza', '', 1),
	             ('mary@gmail.com','mary123', 'Mary', 'Lamb',  '', 1),
	             ('peter@gmail.com','peter123','Peter','Piper', '', 1),
	            ]
	c.executemany('INSERT INTO users VALUES (?,?,?,?,?,?)', users)

	tweets = [('george@gmail.com',0,"tweet0",str(current_time),"NULL"),
	           ('George@gmail.com',1,"tweet1",str(current_time),"NULL"),
	           ('george@gmail.com',2,"tweet2",str(current_time),"NULL"),
	           ('mary@gmail.com',3,"tweet3",str(current_time), "NULL"),]      
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