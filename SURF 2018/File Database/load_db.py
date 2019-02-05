from mysql import connector as sql
import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
from sorter3 import id_angular_groupings, id_discrete_groupings, get_after_new_focus
from datetime import datetime

# Database connection variables
host = 'localhost'
port = 3306
user = # Removed for security reasons #
passwd = # Removed for security reasons #

def create_raw_table(cursor, fname):
	'''
	Generates the column names from the fits file header, as well as adding other useful columns.
	Then, creates the raw_files table in the WIRC_POL database, if it doesn't already exist.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- fname: The file to gather column names from
	'''
	# Check if raw_files already exists and don't create if it does
	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"raw_files\"')
	if cursor.fetchone()[0] == 0:
		raw_data = fits.open(fname)
		# Generate the table columns from the fits header
		header = raw_data[0].header
		sql_columns = []
		for col in header:
			if ('`' + col + '` TEXT') not in sql_columns:
				sql_columns.append('`' + col + '` TEXT')
		query = 'CREATE TABLE IF NOT EXISTS raw_files (tar_id INT(11), File_Path TEXT, Image_Type TEXT, ' + ', '.join(sql_columns) + ', INDEX raw_id (tar_id), FOREIGN KEY (tar_id) REFERENCES targets(id))'
		cursor.execute(query)
		raw_data.close()

def create_calib_table(cursor, fname):
	'''
	Generates the column names from fits file header, as well as adding a column
	for id, filepath, master dark, master flat, hp map and bp map. Creates the
	calib_files table in WIRC_POL, if nonexistent.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- fname: The file to gather column names from
	'''
	# Check if calib_files already exists and don't create if it does
	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"calib_files\"')
	if cursor.fetchone()[0] == 0:
		calib_data = fits.open(fname)
		# Generate the table columns from the fits header
		header = calib_data[0].header
		sql_columns = []
		for col in header:
			if ('`' + col + '` TEXT') not in sql_columns:
				sql_columns.append('`' + col + '` TEXT')
		query = 'CREATE TABLE IF NOT EXISTS calib_files (tar_id INT(11), File_Path TEXT, Created TEXT, Raw_File TEXT, Dark TEXT, Flat TEXT, BP TEXT, HP TEXT, ' \
			    + ', '.join(sql_columns) + ', INDEX cal_id (tar_id), FOREIGN KEY (tar_id) REFERENCES targets(id))'
		cursor.execute(query)
		calib_data.close()

def create_dark_table(cursor):
	'''
	Creates table to hold master darks' information.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	'''
	# Check if master_darks already exists and don't create if it does
	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"master_darks\"')
	if cursor.fetchone()[0] == 0:
		cursor.execute('CREATE TABLE IF NOT EXISTS master_darks (File_Path TEXT, Created TEXT, UTSHUT TEXT, EXPTIME TEXT, HP_MAP TEXT)')

def create_flat_table(cursor):
	'''
	Creates the table to hold master flats' information.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	'''
	# Check if master_flats already exists and don't create if it does
	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"master_flats\"')
	if cursor.fetchone()[0] == 0:
		cursor.execute('CREATE TABLE IF NOT EXISTS master_flats (File_Path TEXT, Created TEXT, UTSHUT TEXT, EXPTIME TEXT, FORE TEXT, AFT TEXT, BP_MAP TEXT)')

def create_sky_table(cursor):
	'''
	Creates the table to hold master skies' information.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	'''
	# Check if the master_skies already exists and don't create if it does
	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"master_skies\"')
	if cursor.fetchone()[0] == 0:
		cursor.execute('CREATE TABLE IF NOT EXISTS master_skies (File_Path TEXT, Created TEXT, UTSHUT TEXT, EXPTIME TEXT)')

def add_raw_file(cursor, fnames, types):
	'''
	Adds the data from a new file to the raw_files table in the WIRC_POL db.
	Takes keys from the fits header and adds new columns if they are not already
	present. Then, goes through the column names and attempts to populate the
	row to be added by referencing the header. If the key is not present, it adds
	'NA' to the row.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- fnames: The files to be added to the database
	- types: A parallel list to fnames, containing the file type of each raw file
	'''
	for i in range(0, len(fnames)):
		print(fnames[i] + '\n')
		raw_data = fits.open(fnames[i])
		raw_data_h = raw_data[0].header
		# Match raw files to targets via a primary/foreign key pair
		raw_id = -1
		if(types[i] in ('pol', 'spec', 'photomet') and 'RA' in raw_data_h.keys() and 'DEC' in raw_data_h.keys()):
			raw_id = find_id(cursor, raw_data_h['RA'], raw_data_h['DEC'])
		row = [raw_id, fnames[i], types[i]]
		# Gather the column names by executing a query (Doing each iteration ensures most recent columns)
		cursor.execute('SELECT * FROM raw_files LIMIT 1')
		cursor.fetchall()
		column_names = cursor.column_names
		# Add any new columns that are not in the existing columns
		for key in raw_data_h.keys():
			if key.encode('utf-8') not in column_names:
				add_column(cursor, key, 'raw_files')
		# Fetch the column names again to ensure they are up to date
		cursor.execute('SELECT * FROM raw_files LIMIT 1')
		cursor.fetchall()
		column_names = [cursor.column_names[k].encode('ascii') for k in range(len(cursor.column_names))]
		# Gather data from the fits header for database upload
		for col in column_names[3:]:
			try:
				data = str(raw_data_h[col])
				row.append(data)
			except KeyError:
				row.append('NA')
		# Prepare the string for the database query
		values = ' VALUES (' + ', '.join(['%s' for x in range(len(row))]) + ')'
		cols = '(`' + '`, `'.join(column_names) + '`)'
		cursor.execute('SELECT COUNT(*) FROM raw_files WHERE `File_Path` = \"{}\"'.format(fnames[i]))
		if cursor.fetchone()[0] > 0:
			cursor.execute('DELETE FROM raw_files WHERE `File_Path` = \"{}\"'.format(fnames[i]))
		cursor.execute('INSERT INTO raw_files ' + cols + values, row)
		raw_data.close()

def add_calib_file(cursor, objs):
	'''
	Adds data from fits headers in calibrated files, to a table in the database.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- objs: A list of calibrated wirc_data objects to extract data from
	'''
	for obj in objs:
		calib_data_h = obj.header
		calib_id = -1
		# Match calibrated files with targets by an primary/foreign key
		if 'RA' in calib_data_h.keys() and 'DEC' in calib_data_h.keys():
			calib_id = find_id(cursor, calib_data_h['RA'], calib_data_h['DEC'])
		row = [calib_id, calib_data_h['CAL_FN'], str(datetime.now()), calib_data_h['RAW_FN'], obj.dark_fn, obj.flat_fn, obj.bp_fn, obj.hp_fn]
		# Gather the column names by executing a query (Doing each iteration ensures most recent columns)
		cursor.execute('SELECT * FROM calib_files LIMIT 1')
		cursor.fetchall()
		column_names = cursor.column_names
		# Add any new columns that are not in the existing columns
		for key in calib_data_h.keys():
			if key.encode('utf-8') not in column_names:
				add_column(cursor, key, 'calib_files')
		# Fetch the column names again to ensure they are up to date
		cursor.execute('SELECT * FROM calib_files LIMIT 1')
		cursor.fetchall()
		column_names = [cursor.column_names[i].encode('ascii') for i in range(len(cursor.column_names))]
		# Gather data from the fits header for database upload
		for col in column_names[8:]:
			try:
				data = str(calib_data_h[col])
				row.append(data)
			except KeyError:
				row.append('NA')
		# Prepare the string for the database query
		values = ' VALUES (' + ', '.join(['%s' for x in range(len(row))]) + ')'
		cols = '(`' + '`, `'.join(column_names) + '`)'
		cursor.execute('SELECT COUNT(*) FROM calib_files WHERE `File_Path` = \"{}\"'.format(calib_data_h['CAL_FN']))
		if cursor.fetchone()[0] > 0:
			cursor.execute('DELETE FROM calib_files WHERE `File_Path` = \"{}\"'.format(calib_data_h['CAL_FN']))
		cursor.execute('INSERT INTO calib_files ' + cols + values, row)

def add_dark(cursor, file, utshut, exp, hp_map):
	'''
	Add a new dark file to the master_darks table.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- file: The file to be added to the master_darks table
	- utshut: The shutter time for the given master dark
	- exp: The exposure for the given master dark
	- hp_map: The hot pixel map associated with the given master dark
	'''
	# Gather the columns from the table
	cursor.execute('SELECT * FROM master_darks LIMIT 1')
	cursor.fetchall()
	columns = '(' + ', '.join(cursor.column_names) + ')'
	# Format the string for the database query
	values = ' VALUES (\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\")'.format(file, str(datetime.now()), utshut, exp, hp_map)
	cursor.execute('SELECT COUNT(*) FROM master_darks WHERE `File_Path` = \"{}\"'.format(file))
	if cursor.fetchone()[0] > 0:
		cursor.execute('DELETE FROM master_darks WHERE `File_Path` = \"{}\"'.format(file))
	cursor.execute('INSERT INTO master_darks ' + columns + values)

def add_flat(cursor, file, utshut, exp, fore, aft, bp_map):
	'''
	Add a new flat file to the master_flats table.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- file: The file to be added to the master_flats table
	- utshut: The shutter time for the given master flat
	- exp: The exposure for the given master flat
	- fore: The fore filter for given master flat
	- aft: The aft filter for the given master flat
	- bp_map: The bad pixel map associated with the given master flat
	'''
	# Gather the columns from the table
	cursor.execute('SELECT * FROM master_flats LIMIT 1')
	cursor.fetchall()
	columns = '(' + ', '.join(cursor.column_names) + ')'
	# Format the string for the database query
	values = ' VALUES (\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\")'.format(file, str(datetime.now()), utshut, exp, fore, aft, bp_map)
	cursor.execute('SELECT COUNT(*) FROM master_flats WHERE `File_Path` = \"{}\"'.format(file))
	if cursor.fetchone()[0] > 0:
		cursor.execute('DELETE FROM master_flats WHERE `File_Path` = \"{}\"'.format(file))
	cursor.execute('INSERT INTO master_flats ' + columns + values)

def add_sky(cursor, file, utshut, exp):
	'''
	Add a new sky file to the master_skies table.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- file: The file to be added to the master_skies table
	- utshut: The shutter time for the given master sky
	- exp: The exposure for the given master sky
	'''
	cursor.execute('SELECT * FROM master_skies LIMIT 1')
	cursor.fetchall()
	columns = '(' + ', '.join(cursor.column_names) + ')'
	values = ' VALUES (\"{0}\", \"{1}\", \"{2}\", \"{3}\")'.format(file, str(datetime.now()), utshut, exp)
	cursor.execute('SELECT COUNT(*) FROM master_skies WHERE `File_Path` = \"{}\"'.format(file))
	if cursor.fetchone()[0] > 0:
		cursor.execute('DELETE FROM master_skies WHERE `File_Path` = \"{}\"'.format(file))
	cursor.execute('INSERT INTO master_skies ' + columns + values)

def find_id(cursor, ra, dec):
	'''
	Finds the tar_id to give a new row when adding it to database. Uses the RA and
	DEC of targets and given data to find the closest match, only adding the id
	if the target is within 4 arcminutes of the raw data.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- ra: The right ascension in use to find a target match
	- dec: The declination in use to find a target match

	Return:
	- The id matched with the given ra and dec (-1 if no match)
	'''

	# WARNING, THIS FUNCTION OFTEN DOES NOT PRODUCE DESIRED EFFECTS
	# Get the needed target information from the database
	cursor.execute('SELECT id, `RA`, `DEC` FROM targets')
	targets = cursor.fetchall()
	# Properly format the target information
	RAs = []
	DECs = []
	for target in targets:
		if target[1] != '' and target[1] != None:
			RAs.append(float(target[1]) * np.pi/180)
		if target[2] != '' and target[2] != None:
			DECs.append(float(target[2]) * np.pi/180)
	RAs = np.array(RAs)
	DECs = np.array(DECs)
	# Get coordinate information in radians
	coord = SkyCoord(str(ra) + str(dec), unit=(u.hourangle, u.deg))
	ra = float(coord.ra.radian)
	dec = float(coord.dec.radian)
	# Find closest target
	dist = np.array([np.arccos(np.sin(dec)*np.sin(DECs[i]) + np.cos(dec)*np.cos(DECs[i])*np.cos(ra - RAs[i]))*(180/np.pi)*60 for i in range(len(RAs))])
	ind = np.where(dist == min(dist))
	# Check if target is close enough. If so, return the id
	if(dist[ind[0][0]] <= 4.0):
		return targets[ind[0][0]][0]
	# If the target is not close enough, print to error log and return -1 (corresponds to None/Unknown)
	f = open('autoreduction_logs/Errors.log', 'a+')
	f.write(str(datetime.now()) + ' - ERROR: The closest target id match to RA: {}, DEC: {}, is not close enough to'
	' be viable (within 2\'). \n'.format(ra, dec))
	f.close()
	return -1

def gen_types(fnames):
	'''
	This identifies the image as dark, flat, pol, spec, or photom. Adapted
	from Michael Randolph's Code in sorter3.py to sort by file type, modified to
	accommodate more error checking.

	Params:
	- fnames: The list of filenames which will have their types identified

	Return:
	- obt: A parallel list to fnames, indicating file types
	'''
	#initiate lists of header values from fits files

	fore = []
	aft = []
	HA = []
	RA = []
	focus = []

	f = open('autoreduction_logs/File_Errors.log', 'a+')
	# Initializing values, including defaults
	for i in range(len(fnames)):
	    # Gather fore filter, accommodating for missing keyword
		hdu = fits.open(fnames[i])
		try:
			fore.append(hdu[0].header["FORE"].split(' ')[0]) #split may not be necessary
		except KeyError:
			fore.append('')
			f.write(str(datetime.now()) + ' - {} has no listed fore filter\n'.format(fnames[i]))
		# Gather aft filter, accommodating for missing keyword
		try:
			aft.append(hdu[0].header["AFT"].split(' ')[0]) #split may not be necessary
		except KeyError:
			aft.append('')
			f.write(str(datetime.now()) + ' - {} has no listed aft filter\n'.format(fnames[i]))
		# Gather hour angle, accommodating for missing keyword
		try:
			HA.append(hdu[0].header["HA"])
		except KeyError:
			HA.append('')
			f.write(str(datetime.now()) + ' - {} has no listed HA\n'.format(fnames[i]))
		# Gather right ascension, accommodating for missing keyword
		try:
			RA.append(hdu[0].header['RA'])
		except KeyError:
			RA.append('')
			f.write(str(datetime.now()) + ' - {} has no listed RA\n'.format(fnames[i]))
		# Gather telescope focus, accommodating for missing keyword
		try:
			focus.append(float(hdu[0].header['TELFOCUS'].split(' ')[0]))
		except KeyError:
			focus.append('')
			f.write(str(datetime.now()) + ' - {} has no listed TELFOCUS\n'.format(fnames[i]))

		hdu.close()
	f.close()
	# See sorter3.py for details on the below functions
	not_tracking_HA_groupings = []
	if len(HA) > 0:
		not_tracking_HA_groupings = id_angular_groupings(HA,1.0,'HA','hard',False)

	contiguous_RA_groupings = []
	if len(RA) > 0:
		contiguous_RA_groupings = id_angular_groupings(RA,4.0*60.0,'RA','soft', False)

	focus_groupings = []
	if len(focus) > 0:
		focus_groupings = id_discrete_groupings(focus)

	after_new_focus = get_after_new_focus(focus_groupings, contiguous_RA_groupings)

	obt = ['unknown'] * len(fnames)
	for i in range(0, len(fnames)):
	    #if dark
		if ((fore[i] == 'BrGamma__(2.17)') and (aft[i] == 'J__(1.25)')):
			obt[i] = 'dark'

	    # if flat (using not_tracking_HA_groupings, 'not_tracking' and != 'f' is sorta a double negative)
		elif ((not_tracking_HA_groupings[i] != 'f') and (fore[i] in ['OPEN', 'PG', 'GRISM'])):
			obt[i] = 'flat'
		else:
	        #if photometry
			if ((fore[i] in ['Diffuser', 'OPEN']) and (aft[i] in ['J__(1.25)', 'H__(1.64)', 'Ks__(2.15)'])):
				obt[i] = 'photomet'
			elif ((fore[i] == 'GRISM') and (aft[i] in ['J__(1.25)', 'H__(1.64)', 'Ks__(2.15)'])):
				obt[i] = 'spec'
			elif ((fore[i] == 'PG') and (aft[i] in ['J__(1.25)', 'H__(1.64)', 'Ks__(2.15)'])):
				obt[i] = 'pol'
			else:
				pass
	return obt

def add_column(cursor, col, table):
	'''
	Adds a new column to the given table, give the column name.

	Params:
	- cursor: The mysql cursor to modify the WIRC_POL database
	- col: The name of the new column to add
	- table: The table to add the new column to
	'''
	cursor.execute('ALTER TABLE `' + table + '` ADD `' + col + '` TEXT')

def initialize_new_column(table, new_col, assign_list):
	'''
	Adds a new column to the table and selectively assigns values according to a
	passed list:

	Params:
	- table: The name of the table to be modified
	- new_col: The name of the new column to be added
	- assign_list: A list with a particular format:
		[['Name LIKE \"%s%\"', 5], ['J > 4', 'O'], ... , ['Condition String', Value]]
	'''
	# Establish database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute("USE WIRC_POL")
	# Use the existing add_column function to add the column
	add_column(cursor, new_col, table)
	# Iterate through assign_list, carrying out the instructions it contains
	for value in assign_list:
		cursor.execute('UPDATE {0} SET {1} = {2} WHERE {3}'.format(table, new_col, value[1], value[0]))
	connection.commit()
	connection.close()


def new_raw_entry(file_paths, types):
	'''
	Takes a file_path list and creates the raw_files table if it does not already exist.
	Then, adds the data from the given file to the raw_files table.

	Params:
	- file_paths: The list of files to be uploaded to the raw_files table
	- types: The list of file types generated by gen_types()
	'''
	print('STARTING UPLOAD TO RAW_FILES')
	# Establish database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute("USE WIRC_POL")

	file_paths.sort()
	# Create the raw_files table, if it does not exist
	create_raw_table(cursor, file_paths[0])
	# Upload all of the files in file_paths to the database
	add_raw_file(cursor, file_paths, types)

	connection.commit()
	connection.close()
	print('UPLOADED FILES TO RAW_FILES TABLE')

def new_calib_entry(objs):
	'''
	Takes file_paths list and creates calib_files table if it does not already exist.
	Then, adds data from given file to raw_files table.

	Params:
	- objs: A list of calibrated wirc_data objects to be uploaded to the calib_files table
	'''
	print('STARTING UPLOAD TO CALIB_FILES')
	# Establish the database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute('USE WIRC_POL')

	# Create the calib_files table, if it does not exist
	create_calib_table(cursor, objs[0].header['CAL_FN'])
	# Upload the header data from all of the objects in objs
	add_calib_file(cursor, objs)

	connection.commit()
	connection.close()
	print('UPLOADED FILES TO CALIB_FILES TABLE')

def new_darks(masterDarks, HPMap):
	'''
	Adds darks to database.

	Params:
	- masterDarks: The list of master dark files to be uploaded
	- HPMap: The associated list of hot pixel maps
	'''
	print('STARTING UPLOAD TO MASTER_DARKS')
	# Establish the database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute('USE WIRC_POL')
	# Create the master_darks table
	create_dark_table(cursor)
	# Upload each of the master darks
	for i in range(len(masterDarks)):
		add_dark(cursor, masterDarks[i], fits.getheader(masterDarks[i])['UTSHUT'], \
				fits.getheader(masterDarks[i])['EXPTIME'], HPMap[i])

	connection.commit()
	connection.close()
	print('UPLOADED MASTER DARKS TO DATABASE')

def new_flats(masterFlats, BPMap):
	'''
	Adds flats to database.

	Params:
	- masterFlats: The list of master flats files to be uploaded
	- BPMap: The associated list of bad piel maps
	'''
	print('STARTING UPLOAD TO MASTER_FLATS')
	# Establish the database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute('USE WIRC_POL')
	# Create the master_flats table
	create_flat_table(cursor)
	# Upload each of the master flats
	for i in range(len(masterFlats)):
		hdu = fits.open(masterFlats[i])
		header = hdu[0].header
		add_flat(cursor, masterFlats[i], header['UTSHUT'], header['EXPTIME'],
				header['FORE'], header['AFT'], BPMap[i])
		hdu.close()

	connection.commit()
	connection.close()
	print('UPLOADED MASTER FLATS TO DATABASE')

def new_skies(masterSkies):
	'''
	Adds skies to database.

	Params:
	- masterSkies: The list of master skies to be uploaded
	'''
	print('STARTING UPLOAD TO MASTER_SKIES')
	# Establish the database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute('USE WIRC_POL')
	# Create the master_skies table
	create_sky_table(cursor)
	# Upload each of the master skies
	for i in range(len(masterSkies)):
		hdu = fits.open(masterSkies[i])
		header = hdu[0].header
		add_sky(cursor, masterSkies[i], header['UTSHUT'], header['EXPTIME'])
		hdu.close()

	connection.commit()
	connection.close()
	print('UPLOADED MASTER SKIES TO DATABASE')
