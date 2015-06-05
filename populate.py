import json
from models import User, Tweet, Subscription
from database import db_session, init_dbs

from random import shuffle
from datetime import datetime


# print(data)

def populate():
	data = json.loads(open("DB/users.json").read())
	u = User('bmahlbrand@gmail.com', 'abc123', 'ben', 'ahlbrand', 'profile.png')
	db_session().add(u)
	u = User('george@gmail.com','abc123','George','Constanza', '')
	db_session().add(u)
	u = User('mary@gmail.com','mary123', 'Mary', 'Lamb',  '')
	db_session().add(u)
	u = User('peter@gmail.com','peter123','Peter','Piper', '')
	db_session().add(u)
	
	db_session().commit()

	# s = Subscription('bmahlbrand@gmail.com', 'george@gmail.com')
	# db_session.add(s)
	# s = Subscription('bmahlbrand@gmail.com', 'mary@gmail.com')
	# db_session.add(s)
	# s = Subscription('bmahlbrand@gmail.com', 'peter@gmail.com')
	# db_session.add(s)

	# s = Subscription('george@gmail.com', 'mary@gmail.com')
	# db_session.add(s)
	# s = Subscription('george@gmail.com', 'peter@gmail.com')
	# db_session.add(s)
	# db_session().commit()

	for row in data:
		user = User.query.filter_by(email=row['email']).first()
		if user is None:
			u = User(row['email'], row['password'], row['first_name'], row['last_name'], row['profilepic_path'])
			db_session().add(u)
	db_session().commit()
	

			# u.follow(u)
			# db_session().commit()
			# print(u.is_following())
	users = User.query.all()
	shuffle(users)
	unusers = users
	shuffle(unusers)
	# print(unusers)
	data = json.loads(open("DB/tweets.json").read())
	for row, user in zip(data, users):
		date_object = datetime.strptime(row['timestamp'], '%I:%M %p')
		tweet = Tweet(user.email, row['text'], date_object)
		db_session().add(tweet)
	db_session().commit()



	topush = []
	for unuser in unusers:
		# print(unuser.email)
		sub = Subscription('bmahlbrand@gmail.com', unuser.email)
		topush.append(sub)
	
	for sub in topush:
		db_session().add(sub)
	
	db_session().commit()

	

	print("database is populated")

