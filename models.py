from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class User(Base):
	__tablename__ = 'users'
	email = Column(String(255), primary_key=True)
	password = Column(String(255))
	first_name = Column(String(255))
	last_name = Column(String(255))
	profilepic_path = Column(String(255))
	activated = Column(Integer)

	def __init__(self, 
		email = None, 
		password = None, 
		first_name = None, 
		last_name = None, 
	 	profilepic_path = None, 
		activated = None
	):

		self.email = email
		self.password = password
		self.first_name = first_name
		self.last_name = last_name
		self.profilepic_path = profilepic_path
		self.activated = activated

	def __repr__(self):
		return "<User(email = '%s', password = '%s', first_name = '%s', last_name = '%s', profilepic_path = '%s', activated = '%d')>" % (self.email, self.password, self.first_name, self.last_name, self.profilepic_path, self.activated)

	# def __eq__(self, other):
	# 	return (self.email == other or
 #        	self.email == getattr(other, 'email', None))

	# def __ne__(self, other):
	# 	return not self.__eq__(other)

	def __hash__(self):
		return id(self)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

class Tweet(Base):
	__tablename__ = 'tweets'
	tweetID = Column(Integer, primary_key=True)
	owner = Column(String(254), unique=True)
	timestamp = Column(DateTime)
	tweet = Column(String(140))
	pic_path = Column(String(255))

	def __init__(self, owner = None, timestamp = None, tweet = None, pic_path = None):
		self.owner = owner
		self.timestamp = timestamp
		self.tweet = tweet
		self.pic_path = pic_path

	def __repr__(self):
		return '<Tweet %r>' % (self.tweetID)

class Subscription(Base):
	__tablename__ = 'subscriptions'

	subscriptionID = Column(Integer, primary_key = True)
	user = Column(String(254))
	subscribed_user = Column(String(254))

	def __init__(self, user=None, subscribed_user=None):
		self.user = user
		self.subscribed_user = subscribed_user

	def __repr__(self):
		return '<Subscription %r>' % (self.email)