import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from datetime import datetime
from contextlib import closing
from popT import populate
from create_user import add_user_to_db
from login import check_password
from account_management import modify_pass

# configuration
DATABASE = 'DB/twittr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

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
	get_db().commit()
	rv = cur.fetchall()
	cur.close()
	print(rv)
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

	get_db().execute('insert into tweets (owner, text, timestamp, pic_path) values (?, ?, ?, ?)',
				 [session.get('user'), request.form['text'], datetime.now(), None])
	get_db().commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
	error = None
	if request.method == 'POST':
		user = query_db('select * from users where email = ?', [request.form['email']], one=True)

		if user is None:
			get_db().execute('insert into users VALUES (?, ?, ?, ?, ?, ?)', 
				[request.form['email'],  request.form['password'],  request.form['first_name'],  request.form['last_name'],  request.form['profilepic_path'], 0])
			get_db().commit()

			success = 'successfully created new account'
			# return redirect(url_for('login'))
			return render_template('login.html', success = success)
		else:
			error = 'user exists'
			return render_template('create_account.html', error = error)			

	elif request.method == 'GET':
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
			return render_template('change_password.html', error = error)
		else:
			error = "passwords don't match"
			return render_template('change_password.html', error = error)
	elif request.method == 'GET':
		return render_template('change_password.html', error = error)

@app.route('/activate', methods=['POST'])
def activate():
	error = None

	g.db.execute('UPDATE USERS set activated=? WHERE email=?', [1, request.form['email']])
	g.db.commit()

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
	
	return render_template('login.html', error = error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	init_db()
	populate()
	app.run()