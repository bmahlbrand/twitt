import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from contextlib import closing
from popT import populate

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
	
	return render_template('login.html', error=error)

def check_password(user, passwd):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	t = (user,)
	c.execute('SELECT * FROM users WHERE email=?', t)

	row = stored_password = c.fetchone()

	conn.close()

	if row != None: 
		stored_password = row[1]
		print(stored_password)
		print(passwd)
		# valid = row[5]
		if (stored_password == passwd):
			# if (valid == 1):
				return 'passed'
		else:
			return 'badpasswd'
	else:
		return 'badusernm'

	return 'failed'

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
	init_db()
	populate()
	app.run()