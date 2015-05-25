import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from contextlib import closing
from popT import populate
from create_user import add_user_to_db
from login import check_password
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
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/add_user', methods=['POST'])
def add_user():
	error = None
	add_user_to_db(request.form)
	return redirect(url_for('login'))

@app.route('/create_account', methods=['GET','POST'])
def create_account():
	error = None
	return render_template('create_account.html', error = error)

@app.route('/activate', methods=['POST'])
def activate():
	error = None
	email = request.form['email']
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	t = (1, email)
	#get list of subscribed tweets
	c.execute('UPDATE USERS set activated=? WHERE email=?', t)
	conn.commit()
	#s = c.fetchall()
   
	#sql = 'SELECT * FROM tweets WHERE owner="'+username+'" OR owner IN (%s) ORDER BY  timestamp DESC' % ',  '.join('?' for a in s[0]) 
	return render_template('validate.html', error = error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		ret = check_password(request.form['username'], request.form['password'])
		if ret == 'passed':
			session['logged_in'] = True
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