from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref
from datetime import datetime

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key = True)
	email = Column(String, unique = True)
	pw_hash = Column(String(70))
	first_name = Column(String(80))
	last_name = Column(String(80))
	profilepic = Column(String(255))
	activated = Column(Integer)
	last_seen = Column(DateTime)

	subscriptions = relationship("Subscription", order_by="Subscription.email_id", backref="email")
	

	# followed = relationship('User', 
	# 						   secondary=followers, 
	# 						   primaryjoin=(followers.c.follower_id == id), 
	# 						   secondaryjoin=(followers.c.followed_id == id), 
	# 						   backref=backref('followers', lazy='dynamic'), 
	# 						   lazy='dynamic')
	
	def __init__(self, 
		email = None, 
		password = None, 
		first_name = None, 
		last_name = None, 
		profilepic = None,
	):

		self.email = email
		self.pw_hash = None
		self.set_password(password)
		self.first_name = first_name
		self.last_name = last_name
		self.profilepic = profilepic
		self.activated = 1
		self.last_seen = datetime.utcnow()

	def __repr__(self):
		return "<User(email = '%s', pw_hash = '%s', first_name = '%s', last_name = '%s', profilepic_path = '%s', activated = '%d')>" % (self.email, self.pw_hash, self.first_name, self.last_name, self.profilepic, self.activated)

	# def __eq__(self, other):
	#   return (self.email == other or
	#   self.email == getattr(other, 'email', None))

	# def __ne__(self, other):
	#   return not self.__eq__(other)

	# def __hash__(self):
		# return hash(self)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password) and self.activated is 1

	def set_profilepic(self, profilepic):
		self.profilepic = profilepic


	# def follow(self, user):
	# 	if not self.is_following(user):
	# 		self.followed.append(user)
	# 		return self

	# def unfollow(self, user):
	# 	if self.is_following(user):
	# 		self.followed.remove(user)
	# 		return self

	# def is_following(self, user):
	# 	return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	# def followed_posts(self):
	# 	return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
	
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

# class Follower(Base):
# 	__tablename__ = 'followers'
# 	id = Column(Integer, primary_key = True)
# 	follower_id = Column(Integer, ForeignKey('user.id'))
# 	followed_id = Column(Integer, ForeignKey('user.id'))