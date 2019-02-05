from mysql import connector as sql
import click
from flask import current_app, g
#g: special object unique to each request
#current_app: points to Flask application handling request
from flask.cli import with_appcontext

def get_db():
	'''
	Create the user database connection and cursor for it.
	'''
	if 'db' not in g:
		g.db = sql.MySQLConnection()
		g.db.connect(host='localhost', user=''' Removed for security reasons '''
									 , passwd='''# Removed for security reasons #''',
								database='wirc_pol_flask')
	return g.db.cursor()

def close_db(e=None):
	'''
	Close the database connection and modify the flask instance appropriately
	'''
	db = g.pop('db', None)

	if db is not None:
		db.close()

# More trouble than it is worth. Not sure if works. Easier to use commands in
# schema.sql to set up manually
def init_db(cursor):
	'''
	Initialize the user database with commands from the schema.sql file.
	'''
	# db = get_db() #returns database connection, used to execute SQL script
	#opens file relative to flask package
	with current_app.open_resource('schema.sql') as f:
		file = f.read()
		commands = file.split(';')
		for command in commands:
			cursor.execute(command)
	g.db.commit()

# Taken from the flask tutorial, but hasn't really worked. Disregard for now
@click.command('init-db') #defines command line command that calls init_db
@with_appcontext
def init_db_command():
	'''Clear existing data and create new tables'''
	init_db()
	click.echo('Initialized the database.')

def init_app(app):
	'''Register close_db and init_db_command with application
	instance. Otherwise, won't be used by app.
	'''
	#tells flask to call close_db when cleaning up after returning
	app.teardown_appcontext(close_db)
	#adds new command to be called with 'flask' command
	app.cli.add_command(init_db_command)
