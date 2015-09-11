#!/usr/bin/python

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug import generate_password_hash, check_password_hash, secure_filename
from datetime import datetime
from contextlib import closing
from os.path import basename
import smtplib 
from email.mime.text import MIMEText

from models import User, Tweet, Subscription
from populate import populate
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGEPATH = "IMAGES"
app = Flask(__name__)
app.config.from_pyfile('conf.cfg', silent = True)

from database import db_session, init_dbs

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@app.teardown_appcontext
def shutdown_session(exception = None):
	db_session.remove()

# @app.before_request
# def check_valid_login():
# 	if (request.endpoint and 'static' not in request.endpoint and not login_valid and not getattr(app.view_functions[request.endpoint], 'is_public', False)):
# 		return render_template('login.html', next=request.endpoint)
# def connect_db():
# 	return sqlite3.connect(app.config['DATABASE'])

# def init_db():
# 	with closing(connect_db()) as db:
# 		with app.open_resource('schema.sql', mode='r') as f:
# 			db.cursor().executescript(f.read())
# 		db.commit()

# def get_db():
#     db = getattr(g, 'db', None)
#     if db is None:
#         db = g.db = connect_db()
#     return db

# def query_db(query, args=(), one=False):
# 	cur = get_db().cursor()
# 	get_db().execute(query, args)
# 	rv = cur.fetchall()
# 	cur.close()
# 	return (rv[0] if rv else None) if one else rv

# @app.before_request
# def before_request():
# 	g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
# 	db = getattr(g, 'db', None)
# 	if db is not None:
# 		db.close()

import os
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon')

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file(profilepic):
	filepath = app.config['UPLOAD_FOLDER'] + "/" + session.get('user') + "/"
	
	if not os.path.exists(filepath):
		os.makedirs(filepath)

	file = profilepic
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + session.get('user'), filename))
		# return redirect(url_for('show_entries', filename=filename))


@app.route('/')
def show_entries():
	results = []
	subscriptions = Subscription.query.filter_by(email_id = session.get('user')).all()

	for user in subscriptions:
		tweets = Tweet.query.filter_by(owner = user.subscribed_user).all()
		results += tweets

	entries = [dict(owner = tweet.owner, text = tweet.text, timestamp = tweet.timestamp) for tweet in results]
	return render_template('show_entries.html', entries = entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)

	tweet = Tweet(session.get('user'), request.form['text'], datetime.now(), None)
	db_session().add(tweet)
	db_session().commit()

	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
	error = None
	if request.method == 'POST':
		user = User.query.filter_by(email = request.form['email']).first()
		if user is None:
			u = User(request.form['email'], 
					request.form['password'], 
					request.form['first_name'],
					request.form['last_name'], 
					request.files['profilepic'].filename)

			upload_file(request.files['profilepic'])
			db_session().add(u)
			db_session().commit()

			flash('successfully created new account')

			if app.config['EMAIL_ENABLED']:
				u.create_user_email(request.form['email'])

			return render_template('login.html', error = error)
		else:
			error = 'user exists'

	return render_template('create_account.html', error = error)

@app.route('/manage_account', methods=['GET'])
def manage_account():
	error = None
	return render_template('manage_account.html', error = error)

@app.route('/change_profilepic', methods=['GET', 'POST'])
def change_profilepic():
	error = None

	if request.method == 'POST':
		user = User.query.filter_by(email=session.get('user')).first() # .update(dict(profilepic=request.files['profilepic'].filename))
	
		user.profilepic = request.files['profilepic'].filename

		db_session().commit()
		
		print(user)
		upload_file(request.files['profilepic'])
		flash('successfully changed profile picture!')
		return redirect(url_for('manage_account'))
	else:
		return render_template('change_profilepic.html', error = error)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
	error = None

	if request.method == 'POST':
		if request.form['password'] == request.form['confirm']:
			user = User.query.filter_by(email=session.get('user')).first()
		else:
			error = "passwords don't match"

		if user is not None:
			ret = user.check_password(request.form['oldpassword'])
		
		if ret == True:
			user.set_password(request.form['password'])

			flash('password change successful')
			return redirect(url_for('show_entries'))
		else:
			error = 'invalid password'

	return render_template('change_password.html', error = error)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
	error = None
	if request.method == 'POST':
		username = session.get('user')
		subscribee = request.form['subscribee']
		
		s = Subscription(username, subscribee)

		db_session().add(s)
		db_session().commit()
		
		flash('You subscribed!')
		return redirect(url_for('manage_account'))
	elif request.method == 'GET':

		subscribed_users = [result.subscribed_user for result in Subscription.query.filter_by(email_id = session.get('user')).all()]
		rv = db_session().query(User).filter(User.email != session.get('user')).all()

		results = []
		for row in rv:
			if row.email not in subscribed_users:
				results.append(row)

		users = [dict(email = row.email, first_name = row.first_name, last_name = row.last_name, profilepic = row.profilepic)  for row in results]
		return render_template('subscribe.html', entries = users)

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
	error = None
	if request.method == 'POST':
		username = session.get('user')
		subscribee = request.form['subscribee']

		s = Subscription.query.filter(Subscription.email_id == username,
										Subscription.subscribed_user == subscribee).first()
		db_session().delete(s)
		db_session().commit()

		flash('You unsubscribed!')
		return redirect(url_for('manage_account'))
	elif request.method == 'GET':
		subscribed_users = [result.subscribed_user for result in Subscription.query.filter_by(email_id = session.get('user')).all()]
		rv = db_session().query(User).filter(User.email != session.get('user')).all()

		results = []

		for row in rv:
			if row.email in subscribed_users:
				results.append(row)

		users = [dict(email = row.email, first_name = row.first_name, last_name = row.last_name, profilepic = row.profilepic)  for row in results]

		return render_template('unsubscribe.html', entries = users)

@app.route('/activate', methods=['POST'])
def activate():
	error = None

	get_db().execute('UPDATE USERS set activated=? WHERE email=?', [1, request.form['email']])
	get_db().commit()

	return render_template('validate.html', error = error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None

	if request.method == 'POST':

		user = User.query.filter_by(email=request.form['username']).first()
		
		if user is not None:
			ret = user.check_password(request.form['password'])
			if ret == True:
				session['logged_in'] = True
				session['user'] = user.email
				flash('You were logged in')
				return redirect(url_for('show_entries'))
			else:
				error = "Invalid password"
		else:
			error = "Invalid email"

	if 'logged_in' in session and session['logged_in'] == True:
		return redirect(url_for('show_entries'))
	else:
		return render_template('login.html', error = error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('user', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	init_dbs()
	# print(User.query.all())
	# print(Subscription.query.all())
	# populate()
	app.run()