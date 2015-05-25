#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('DB/twittr.db')

c = conn.cursor()

# Turn on foreign key support
c.execute("PRAGMA foreign_keys = ON")

# Create users table
c.execute('''CREATE TABLE users
	     (email TEXT NOT NULL,
	      first_name TEXT NOT NULL,
	      last_name TEXT NOT NULL, 
	      password TEXT NOT NULL,
	      profilepic_path TEXT NOT NULL,
          activated INTEGER NOT NULL,
	      PRIMARY KEY(email))''')

#
# create tweet
# Visibility is 'public' or 'private'
c.execute('''CREATE TABLE tweets
	     (owner TEXT NOT NULL,
	      tweet_id INTEGER PRIMARY KEY AUTOINCREMENT,
	      tweet_text VARCHAR(140) NOT NULL,
	      timestamp TIMESTAMP NOT NULL,
              pic_path TEXT
	      )''')
	
#FOREIGN KEY (owner) REFERENCES users(email),

# create subscriptions
c.execute('''CREATE TABLE subscriptions
	     (user TEXT NOT NULL,
	      subscribed_user TEXT NOT NULL)''')
	   #FOREIGN KEY(email) REFERENCES users(email),   

# Create sessions table
# add ip address later?
c.execute('''CREATE TABLE sessions
	     (user TEXT NOT NULL,
	      session TEXT NOT NULL,
	      FOREIGN KEY(user) REFERENCES users(email),
	      PRIMARY KEY(session))''')


# Save the changes
conn.commit()

# Close the connection
conn.close()
