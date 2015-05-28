#!/usr/bin/python

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from contextlib import closing
from popT import populate
from create_user import add_user_to_db
from login import check_password
from account_management import modify_pass
import smtplib 
from email.mime.text import MIMEText

app = Flask(__name__)
app.config.from_pyfile('conf.cfg', silent=True)

# from database import db_session, init_db
import database
from models import User

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db

def query_db(query, args=(), one=False):
	cur = get_db().cursor()
	get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def show_entries():
	cur = get_db().execute('select owner, text, timestamp from tweets order by timestamp desc')
	tweets = [dict(owner = row[0], text = row[1], timestamp = row[2]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries = tweets)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)

	cur = get_db().cursor()
	cur.execute('insert into tweets (owner, text, timestamp, pic_path) values (?, ?, ?, ?)',
				 [session.get('user'), request.form['text'], datetime.now(), None])
	get_db().commit()

	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

def create_user_email(email):
	body =  """
			To complete setting up your account, please click the following link to confirm your email is valid:
			"http://data.cs.purdue.edu:8892/petetwitt/validate.cgi?action=activate&email={0}"
			""".format(email)

	msg = MIMEText(body)

	msg['Subject'] = 'Validate your PeteTwitt account' #% registration_confirmation
	msg['From'] = app.config['MAIL_USERNAME']
	msg['To'] = email

	s = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
	s.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
	s.sendmail(app.config['MAIL_USERNAME'], [email], msg.as_string())
	s.quit()

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
	error = None
	if request.method == 'POST':
		user = query_db('select * from users where email = ?', [request.form['email']], one=True)

		if user is None:
			# u = User(str(request.form['email']), 
			# 		str(request.form['password']), 
			# 		str(request.form['first_name']),
			# 		str(request.form['last_name']), 
			# 		str(request.form['profilepic_path']), 
			# 		0
			# 		)
			# database.db_session().add(u)
			# database.db_session.commit()
			# User.query.all()
			get_db().execute('insert into users VALUES (?, ?, ?, ?, ?, ?)', 
				[request.form['email'],  generate_password_hash(request.form['password']),  request.form['first_name'],  request.form['last_name'],  request.form['profilepic_path'], 0])
			get_db().commit()

			flash('successfully created new account')
			# print('balls')
			create_user_email(request.form['email'])
			return render_template('login.html', error = error)
		else:
			error = 'user exists'

	return render_template('create_account.html', error = error)

@app.route('/manage_account', methods=['GET'])
def manage_account():
	error = None
	return render_template('manage_account.html', error = error)
	
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
	error = None

	if request.method == 'POST':

		ret = check_password(session.get('user'), request.form['oldpassword'])
		if ret == 'passed' and request.form['password'] == request.form['confirm']:
			get_db().execute('UPDATE USERS set password=? WHERE email=?', [request.form['password'], session.get('user')])
			get_db().commit()
			flash('password change successful')
			return redirect(url_for('show_entries'))
		
		elif ret == 'badpasswd':
			error = 'invalid password'
		else:
			error = "passwords don't match"

	return render_template('change_password.html', error = error)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
	error = None
	if request.method == 'POST':
		username = session.get('user')
		subscribee = request.form['subscribee']
		
		cur = get_db().cursor()
		cur.execute('INSERT INTO subscriptions (user, subscribed_user) VALUES (?, ?)', [username, subscribee])
		get_db().commit()
		
		flash('You subscribed!')
		return redirect(url_for('manage_account'))
	elif request.method == 'GET':
		cur = get_db().cursor()
		cur.execute('SELECT subscribed_user FROM subscriptions WHERE user = ?', [session.get('user')])
		get_db().commit()
		subscribed_users = [row[0] for row in cur.fetchall()]

		rv = []
		cur.execute('SELECT email, first_name, last_name, profilepic_path FROM users WHERE email != ?', [session.get('user')])

		for row in cur.fetchall():
			if row[0] not in subscribed_users and row[0] != session.get('user'):
				rv.append(row)

		users = [dict(email = row[0], first_name = row[1], last_name = row[2], profilepic_path = row[3])  for row in rv]
		return render_template('subscribe.html', entries = users)

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
	error = None
	if request.method == 'POST':
		username = session.get('user')
		subscribee = request.form['subscribee']

		cur = get_db().cursor()
		cur.execute('DELETE FROM subscriptions WHERE user=? AND subscribed_user=?', [username, subscribee])
		get_db().commit()
		flash('You unsubscribed!')
		return redirect(url_for('manage_account'))
	elif request.method == 'GET':
		cur = get_db().cursor()
		cur.execute('SELECT subscribed_user FROM subscriptions WHERE user=?', [session.get('user')])
		subscribed_users = [row[0] for row in cur.fetchall()]

		rv = []
		cur.execute('SELECT email, first_name, last_name, profilepic_path FROM users WHERE email != ?', [session.get('user')])

		for row in cur.fetchall():
			if row[0] in subscribed_users and row[0] != session.get('user'):
				rv.append(row)

		users = [dict(email = row[0], first_name = row[1], last_name = row[2], profilepic_path = row[3])  for row in rv]

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
		ret = check_password(request.form['username'], request.form['password'])
		if ret == 'passed':
			session['logged_in'] = True
			session['user'] = request.form['username']
			flash('You were logged in')
			return redirect(url_for('show_entries'))
		elif ret == 'badusernm':
			error = 'Invalid username'
		elif ret == 'badpasswd':
			error = 'Invalid password'
	if 'logged_in' in session and session['logged_in'] == True:
		return redirect(url_for('show_entries'))
	else:
		return render_template('login.html', error = error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	
	init_db()
	# populate()
	app.run()