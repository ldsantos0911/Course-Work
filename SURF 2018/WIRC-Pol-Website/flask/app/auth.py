import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session,
	url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
import socket

#creates blueprint named auth, /auth prepended to all associated URLs
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST')) #associate URL '/register' w/ register func
#when Flask receives request to /auth/register, it will call 'register' view and use
#return value as response
def register():
	'''
	Handles the registration form.
	'''
	if request.method == 'POST': #i.e. if user has submitted form
		username = request.form['username']
		password = request.form['password']
		code = request.form['code']
		db = get_db()
		error = None
		# Count existing instances of a perticular user
		db.execute('SELECT COUNT(*) FROM user WHERE username = \"{}\"'.format(username))
		user_count = db.fetchone()[0]
		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required'
		elif code != ''' # Removed for security reasons # ''':
			error = 'Invalid Registration Code'
		elif user_count > 0:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			# Add new user to database
			db.execute('INSERT INTO user (username, password) VALUES (\"{}\", \"{}\")'.format(username, generate_password_hash(password)))
			g.db.commit()
			hostname = socket.gethostname()
			# Handles online vs local hosting
			if hostname == 'riri':
				return redirect('http://riri.caltech.edu/auth/login')
			else:
				return redirect(url_for('auth.login'))
		flash(error)
	return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	'''
	Handles the login form.
	'''
	if request.method == 'POST': # If form is submitted
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		db.execute(
			'SELECT id, username, password FROM user WHERE username = \"{}\"'.format(username)
		)
		user = db.fetchone()

		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user[2], password):
			error = 'Incorrect password.'

		if error is None:
			# Login as user
			session.clear() #session is a dict that stores data across requests
			session['user_id'] = user[0]
			# Handles online vs local hosting
			hostname = socket.gethostname()
			if hostname == 'riri':
				return redirect('http://riri.caltech.edu/')
			else:
				return redirect(url_for('home'))
		flash(error)
	return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
	'''
	Checks if a user id is stored in session and stores it on g.user.
	Verifies that a user is signed in.
	'''
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		db = get_db()
		db.execute(
			'SELECT * FROM user WHERE id = {}'.format(user_id)
		)
		g.user = db.fetchone()

@bp.route('/logout')
def logout():
	'''
	Handles logging out in the flask app.
	'''
	session.clear()
	# Handles online and local hosting
	hostname = socket.gethostname()
	if hostname == 'riri':
		return redirect('http://riri.caltech.edu/')
	else:
		return redirect(url_for('home'))

#decorator to check logged in for each view
def login_required(view):
	#Check which computer you're on
	hostname = socket.gethostname()
	# This could be greatly simplified
	if hostname == 'riri':
		print("RIRI!")
		@functools.wraps(view)
		def wrapped_view(**kwargs):
			if g.user is None:
				hostname = socket.gethostname()
				if hostname == 'riri':
					return redirect('http://riri.caltech.edu/auth/login')
				else:
					return redirect(url_for('auth.login')) #url_for generates URL to a view based on name and args
				#name associated with niew is also called endpoint, by default same as view function name

			return view(**kwargs)
		return wrapped_view
	else:
		return(view)
