from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref

class User(Base):
	__tablename__ = 'users'

	email = Column(String, primary_key = True)
	pw_hash = Column(String)
	first_name = Column(String)
	last_name = Column(String)
	profilepic_path = Column(String)
	activated = Column(Integer)

	subscriptions = relationship("Subscription", order_by="Subscription.email_id", backref="email")
	def __init__(self, 
		email = None, 
		password = None, 
		first_name = None, 
		last_name = None, 
	 	profilepic_path = None,	
	):

		self.email = email
		self.pw_hash = None
		self.set_password(password)
		self.first_name = first_name
		self.last_name = last_name
		self.profilepic_path = profilepic_path
		self.activated = 1

	def __repr__(self):
		return "<User(email = '%s', pw_hash = '%s', first_name = '%s', last_name = '%s', profilepic_path = '%s', activated = '%d')>" % (self.email, self.pw_hash, self.first_name, self.last_name, self.profilepic_path, self.activated)

	# def __eq__(self, other):
	# 	return (self.email == other or
	# 	self.email == getattr(other, 'email', None))

	# def __ne__(self, other):
	# 	return not self.__eq__(other)

	# def __hash__(self):
		# return hash(self)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password) and self.activated is 1

class Tweet(Base):
	__tablename__ = 'tweets'
	tweetID = Column(Integer, primary_key=True)
	owner = Column(String(254))
	text = Column(String(140))
	timestamp = Column(DateTime)
	pic_path = Column(String(255))

	def __init__(self, owner = None, text = None, timestamp = None, pic_path = None):
		self.owner = owner
		self.text = text
		self.timestamp = timestamp
		self.pic_path = pic_path

	def __repr__(self):
		return '<Tweet %r>' % (self.tweetID)

class Subscription(Base):
	__tablename__ = 'subscriptions'

	subscriptionID = Column(Integer, primary_key = True)
	email_id = Column(String(254), ForeignKey('users.email'))
	subscribed_user = Column(String(254))

	user_name = relationship("User", backref=backref('users'))
	def __init__(self, email=None, subscribed_user=None):
		self.email_id = email
		self.subscribed_user = subscribed_user

	def __repr__(self):
		return '<Subscription %r>' % (self.email)