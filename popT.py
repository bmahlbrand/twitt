#!/usr/bin/python

import sqlite3
import datetime
current_time = datetime.datetime.now().time()
print
print "Run only once or you will get error for duplicates"
print 

conn = sqlite3.connect('petetwitt.db')
c = conn.cursor()
# Add one user
user=('dave@gmail.com','David','Blaine', 'dave123')
c.execute('INSERT INTO users VALUES (?,?,?,?)', user)

# Larger example that inserts many records at a time
users = [('george@gmail.com','George','Constanza', 'abc123'),
             ('mary@gmail.com','Mary', 'Lamb', 'mary123'),
             ('peter@gmail.com','Peter','Piper', 'peter123' ),
            ]
c.executemany('INSERT INTO users VALUES (?,?,?,?)', users)

tweets = [('george@gmail.com',0,"tweet0",str(current_time),"NULL"),
           ('george@gmail.com',1,"tweet1",str(current_time),"NULL"),
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

print 'Done.'
