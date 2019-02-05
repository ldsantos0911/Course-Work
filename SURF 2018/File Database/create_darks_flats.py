import wirc_drp.wirc_object as wo
import numpy as np
#import wirc_drp.utils.calibration as calibration
import calibration
from astropy.io import fits
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord
from datetime import datetime
import os
import load_db
from mysql import connector as sql

# Global variables

# Radius within which images will be considered of the same object
object_group_radius = 8.0
# Number of standard deviations an image must deviate from the mean location by in ordered to be considered sky
sky_sigmas = 3

# Parameters of database connection
host = 'localhost'
port = 3306
user = # Removed for security reasons #
passwd = # Removed for security reasons #

def split_by_type(fnames, types):
	'''
	Separates the given files into lists according to the image type.

	fnames: Files to separate
	types: Parallel list which gives all of the types.
	'''
	darks = []
	flats = []
	sci = []
	for i in range(0, len(types)):
		if types[i] == 'dark':
			darks.append(fnames[i])
		elif types[i] == 'flat':
			flats.append(fnames[i])
		elif types[i] == 'pol':
			sci.append(fnames[i])
	return darks, flats, sci

def find_dark_files(darks, master_dark_files):
	'''
	Given a list of darks, groups them by exposure time, in consecutive chunks.
	Each item in the resulting list is a list of files which will be used to
	create a master dark.

	darks: All of the recognized darks
	master_dark_files: List of lists of darks. Will be recursively populated then returned.
	'''
	if len(darks) == 0:
		return master_dark_files

	if len(darks) == 1:
		master_dark_files.append([darks[0]])
		return find_dark_files([], master_dark_files)

	dark_list = [darks[0]]
	dark_ind = 1
	first = fits.open(darks[0])
	second = fits.open(darks[1])
	exposure = first[0].header['EXPTIME']
	first.close()
	curr_exp = second[0].header['EXPTIME']
	second.close()

	while curr_exp == exposure:
		# Generate groups of consecutive darks with the same exposure to be combined later
		dark_list.append(darks[dark_ind])
		dark_ind += 1
		if dark_ind == len(darks):
			break
		# Get next exposure for comparison
		curr = fits.open(darks[dark_ind])
		curr_exp = curr[0].header['EXPTIME']
		curr.close()

	master_dark_files.append(dark_list)
	# Perform the function again, removing the files which have already been used
	return find_dark_files(darks[dark_ind:], master_dark_files)

def find_flat_files(flats, master_flat_files):
	'''
	Given a list of flats, groups them by exposure time, filters, and mask, in consecutive chunks.
	Each item in the resulting list is a list of files which will be used to
	create a master flat.

	Params:
	- flats: All of the recognized flats
	- master_flat_files: List of lists of flats. Will be recursively populated then returned.

	Return:
	- master_flat_files: The 2-d list of each consecutive group of flat files
	'''
	# There is so much commented code because there were a few iterations of this function
	# in search of one that worked

	if len(flats) == 0:
		return master_flat_files

	if len(flats) == 1:
		master_flat_files.append([flats[0]])
		return find_flat_files([], master_flat_files)

	flat_list = []
	# flatPGlist = []
	flat_ind = 0
	first = fits.open(flats[0])
	#second = fits.open(flats[flat_ind])
	exposure = first[0].header['EXPTIME']
	fore = first[0].header['FORE']
	aft = first[0].header['AFT']
	try:
		mask = first[0].header['MASKPOS']
	except KeyError:
		mask = ''
	first.close()
	# curr_exp = second[0].header['EXPTIME']
	# curr_fore = second[0].header['FORE']
	# curr_aft = second[0].header['AFT']
	# second.close()
	curr_exp = exposure
	curr_fore = fore
	curr_aft = aft
	curr_mask = mask

	while curr_exp == exposure and curr_aft == aft and curr_fore == fore and curr_mask == mask:
		# Find consecutive groups of flats with same exposure, filters, and masks
		# if(curr_fore == 'PG'):
		# 	flatPGlist.append(flats[flat_ind])
		# elif curr_fore == fore:
		# 	flat_list.append(flats[flat_ind])
		# else:
		# 	break
		flat_list.append(flats[flat_ind])
		flat_ind += 1
		if flat_ind == len(flats):
			break
		# Get information for next flat for comparison
		curr = fits.open(flats[flat_ind])
		curr_exp = curr[0].header['EXPTIME']
		curr_fore = curr[0].header['FORE']
		curr_aft = curr[0].header['AFT']
		try:
			# MASKPOS not always guaranteed to be present, so check for it, enabling automatic process
			curr_mask = curr[0].header['MASKPOS']
		except KeyError:
			curr_mask = ''
		curr.close()

	# if len(flat_list) > 0:
	master_flat_files.append(flat_list)
	# if len(flatPGlist) > 0:
	# 	master_flat_files.append(flatPGlist)
	# Run the function again, excluding files that have already been used
	return find_flat_files(flats[flat_ind:], master_flat_files)

def find_obj_groups(sci, master_sci_files):
	'''
	This function groups science images by object, identifying these groups as
	images within an arcminute radius defined globally.

	Params:
	- sci: List of all of the science image (after problematic files are removed)
	- master_sci_files: An initially blank list which will be poulated by lists of science files
						grouped by object.

	Return:
	- master_sci_files: A 2-d list containing science files grouped by object (includes sky images for now):
		[[sci files for obj 1], [sci files for obj 2], ...]
	'''
	if len(sci) == 0:
		# Base case
		return master_sci_files

	if len(sci) == 1:
		master_sci_files.append([sci[0]])
		return find_obj_groups([], master_sci_files)

	sci_list = [sci[0]]
	sci_new = []
	sci_ind = 1

	first = fits.open(sci[0])
	ra = first[0].header['RA']
	dec = first[0].header['DEC']
	first.close()

	second = fits.open(sci[1])
	curr_ra = second[0].header['RA']
	curr_dec = second[0].header['DEC']
	second.close()

	# Use SkyCoord to determine angular separation between first and second
	coord = SkyCoord(str(ra) + str(dec), unit=(u.hourangle, u.deg))
	curr_coord = SkyCoord(str(curr_ra) + str(curr_dec), unit=(u.hourangle, u.deg))
	dist = coord.separation(curr_coord).arcminute
	while True:
		if dist <= object_group_radius:
			# Append to the list, if a file is within the necessary radius
			sci_list.append(sci[sci_ind])
		else:
			# Otherwise, append to the list which will be searched in the next run
			sci_new.append(sci[sci_ind])
		sci_ind += 1
		if sci_ind == len(sci):
			# at the end of the list
			break
		# Get information for the current coordinate, and find the current separation
		curr = fits.open(sci[sci_ind])
		curr_ra = curr[0].header['RA']
		curr_dec = curr[0].header['DEC']
		curr_coord = SkyCoord(str(curr_ra) + str(curr_dec), unit=(u.hourangle, u.deg))
		dist = coord.separation(curr_coord).arcminute
		curr.close()

	master_sci_files.append(sci_list)

	return find_obj_groups(sci_new, master_sci_files)

def find_consec_sky(sci_images, dists, mean_dist, dist_sigma):
	'''
	This function finds the groups of consecutively taken sky images within the groups
	of science images.

	Params:
	- sci_images: The 1-d list of one group of science images (by object)
	- dists: List of all of the distances from the mean location of a group of science images
	- mean_dist: The mean distance from the mean location
	- dist_sigma: The standard deviation in distances from the mean dist

	Return:
	- master_sky_groups: A 2-d list structured as follows:
		[[sky files for obj, group 1], [sky files for obj, group 2]]
	'''
	master_sky_groups = []
	i = 0
	while i < len(sci_images):
		master_sky = []
		while (dists[i] - mean_dist) >= (sky_sigmas*dist_sigma):
			# While the above condition holds true, it indicates that we are within a group of sky files
			master_sky.append(sci_images[i])
			i += 1
			if i == len(sci_images):
				break
		i += 1
		# Append this group of sky images to the master list, if not empty
		if len(master_sky) > 0:
			master_sky_groups.append(master_sky)
	return master_sky_groups

def find_sky(sci):
	'''
	This function goes through the process of identifying the groups of sky images which
	will be median combined into master skies, as well as the science files that correspond
	to them, using other functions.

	Params:
	- sci: The list of all polarimetry files entered into the pipeline.

	Return:
	- master_sky_files: A 3-d list structured as follows:
		[[[skies for obj 1, group 1], [skies for obj 1, group 2]], [[skies for obj2, group 1], [skies for obj2, group 2]]]
	- master_sci_files: A 2-d list structured as follows (science files includes skies for now):
		[[science files for obj 1], [science files for obj 2]]
	'''
	ind = 0
	sci_raw = sci
	sci = []
	while ind < len(sci_raw):
		# Go through the list of science files and effectively remove any that cause errors due to missing RA or DEC
		try:
			first = fits.open(sci_raw[ind])
			ra = first[0].header['RA']
			dec = first[0].header['DEC']
			sci.append(sci_raw[ind])
			ind += 1
			first.close()
		except KeyError:
			print('File Error; removing {} from sky generations.'.format(sci_raw[ind]))
			f = open('autoreduction_logs/File_Errors.log', 'a+')
			f.write(str(datetime.now()) + 'File Error; removing {} from sky generations.'.format(sci_raw[ind]))
			f.close()
			first.close()
			ind += 1
	# find_obj_groups separates the master list of sci files by object (8' radius)
	master_sci_files = find_obj_groups(sci, [])
	master_sky_files = []
	for i, sci_list in enumerate(master_sci_files):
		sci_list.sort()
		# Get all of the RAs and DECs in degrees
		sky_coords = [SkyCoord(str(fits.getheader(x)['RA']) + str(fits.getheader(x)['DEC']), unit=(u.hourangle, u.deg)) for x in sci_list]
		RAs = np.array([float(x.ra.degree) for x in sky_coords])
		DECs = np.array([float(x.dec.degree) for x in sky_coords])
		# Identify the mean location (sort of center point) of all of the images in a list of sci files
		mean_RA = np.mean(RAs)
		mean_DEC = np.mean(DECs)
		mean_coord = SkyCoord(mean_RA, mean_DEC, unit='deg')
		# Find a list of all of the angular distances from the mean location
		dists = [mean_coord.separation(x).arcminute for x in sky_coords]
		# Pass the mean distance and standard deviation into find_consec_sky, which will identify the consecutively
		# taken sky files in each science list.
		mean_dist = np.mean(dists)
		dist_sigma = np.std(dists)
		master_sky_files.append(find_consec_sky(sci_list, dists, mean_dist, dist_sigma))
		for sky_list in master_sky_files[-1]:
			# Remove the sky files from the corresponding list of science files (so we don't reduce sky files later on)
			for sky_file in sky_list:
				master_sci_files[i].remove(sky_file)

	return master_sky_files, master_sci_files

def generate_darks(darks, date):
	'''
	Generates the master darks and HP maps, given a list of the darks. Uses find_dark_files to
	group the darks into appropriate lists.

	Params:
	- darks: List of all dark files given to the pipeline
	- date: The night for which the darks are being generated

	Return:
	- masterDarks: A list of all of the master darks generated by the pipeline
	- hpMaps: A parallel list of the hot pixel maps generated with the master darks
	- master_dark_files: Another parallel list containing the darks that went into each
			             corresponding master dark
	'''
	master_dark_files = find_dark_files(darks, [])
	masterDarks = []
	hpMaps = []
	for master in master_dark_files:
		# For each list of dark files in the master 2-d list, create a master dark
		MDTemp, HPTemp = calibration.masterDark(master, output_dir='calibrations/Auto_Reduced/master_darks/' + date + '_')
		masterDarks.append(MDTemp)
		# Write the list of files that went into making master dark
		f = open(MDTemp[:-5] + '_files.list', 'w+')
		f.write('\n'.join(master))
		f.close()
		hpMaps.append(HPTemp)

	return masterDarks, hpMaps, master_dark_files

def generate_flats(flats, date, masterDarks, HPMap):
	'''
	Generates the master flats and BP maps, given a list of the flats, etc. Uses find_flat_files to
	group the flats into appropriate lists.

	Params:
	- flats: The flats.
	- date: The night for which the flats are being generated
	- masterDarks: The list of master darks; used for flat generation
	- HPMap: The parallel list of hot pixel maps.

	Return:
	- masterFlats: The list of master flats generated by the pipeline
	- bpMaps: The parallel list of bad pixel maps generated with the master flats
	- master_flat_files: Another parallel 2-d list containing the flat files used
						 in generating the master flats
	'''
	master_flat_files = find_flat_files(flats, [])
	masterFlats = []
	bpMaps = []

	# Identify the indices of all of the PG flat groups
	index = []
	for i in range(len(master_flat_files)):
		if fits.getheader(master_flat_files[i][0])['FORE'] == 'PG':
			index.append(i)

	# Create a new temporary list, and populate master_flat_files with all of the non-PG flats
	mas_flat_fil = master_flat_files
	master_flat_files = []
	for i in range(len(mas_flat_fil)):
		if i not in index:
			master_flat_files.append(mas_flat_fil[i])

	# Add the PG flat groups onto the end of master_flat_files
	# This is done to ensure mask flats are always created before PG flats
	for i in range(len(mas_flat_fil)):
		if i in index:
			master_flat_files.append(mas_flat_fil[i])

	for master in master_flat_files:
		# Handle each group of flat files in master_flat_files
		masterDark = ''
		hp_map = ''
		flat = fits.open(master[0])
		# Find a masterDark with equal exposure time to the flats to be combined
		for i in range(0, len(masterDarks)):
			dark = fits.open(masterDarks[i])
			if dark[0].header['EXPTIME'] == flat[0].header['EXPTIME']:
				dark.close()
				masterDark = masterDarks[i]
				hp_map = HPMap[i]
				break
		MFTemp = ''
		BPTemp = ''

		# If no master dark with equal exposure is found, find the one with closest exposure
		if masterDark == '':
			masterDarksNP = np.array([fits.getheader(x)['exptime'] for x in masterDarks])
			diff = masterDarksNP - flat[0].header['exptime']
			for i in range(len(diff)):
				diff[i] = abs(diff[i])
			ind = np.where(diff == min(diff))[0][0]
			masterDark = masterDarks[ind]
			hp_map = HPMap[ind]

		if flat[0].header['FORE'] == 'PG':
			try:
				'''
				This is to generate a PG Flat, which requires locating the mask flat, if it can be found.
				It searches for the closest flat in exposure time which has the mask in but not a PG FORE.
				If it can't be found or there isn't a mask flat, it searches the database. If that fails, it
				prompts the user.
				'''
				zeros = np.array([(x, fits.getheader(x)['exptime']) for x in masterFlats if fits.getheader(x)['fore'] != 'PG'\
				and 'IN' in fits.getheader(x)['MASKPOS'].upper()])
				if len(zeros) == 0:
					raise KeyError
				dist = []
				# Find the closest mask flat in exposure time
				for zero in zeros:
					dist.append(abs(float(zero[1]) - fits.getheader(master[0])['exptime']))
				dist = np.array(dist)
				zero_flat = ''
				zero_flat = zeros[np.where(dist == min(dist))[0][0]][0]
				if zero_flat == '':
					raise KeyError
				MFTemp, BPTemp = calibration.masterPGFlat(master, masterDark, hotp_map_fname=hp_map, zeroth_order_flat_fname=zero_flat, output_dir='calibrations/Auto_Reduced/master_flats/' + date + '_')
			except KeyError:
				zero_flat = ''
				zero_flat, zero_bp = get_from_flatdb(master[0], mask=True)
				# If database query was unsuccessful
				if zero_flat == '':
					while True:
						try:
							zero_flat = str(raw_input('Please input the filename for the zeroth order flat for the following files: \n{}\n-> '.format(master)))
							f = fits.open(zero_flat)
							f.close()
							break
						except:
							print('Invalid filename. Format: \"YYYYMMDD/wirc1234.fits\"\n')
							continue
				MFTemp, BPTemp = calibration.masterPGFlat(master, masterDark, hotp_map_fname=hp_map, zeroth_order_flat_fname=zero_flat, output_dir='calibrations/Auto_Reduced/master_flats/' + date + '_')
				master.append(zero_flat)
		else:
			MFTemp, BPTemp = calibration.masterFlat(master, masterDark, hotp_map_fname=hp_map, output_dir='calibrations/Auto_Reduced/master_flats/' + date + '_')

		masterFlats.append(MFTemp)
		# Write the files that went into making the master flat, to a file
		f = open(MFTemp[:-5] + '_files.list', 'w+')
		f.write('\n'.join(master))
		f.close()
		bpMaps.append(BPTemp)
		flat.close()

	return masterFlats, bpMaps, master_flat_files

def generate_sky(sci, date):
	'''
	This is the wrapper function for identifying the consecutive sky images by object group
	then median combining them into the master skies which will be used.

	Params:
	- sci: List of all of the science image passed to the pipeline
	- date: The night associated with the aforementioned science images

	Return:
	- masterSkies: A 2-d list of all of the master skies, with each element containing
				   the master skies for a given object group.
	- master_sci_files: A parallel 2-d list to masterSkies, indicating the science images
						corresponding to a particular group of sky files.
	'''
	master_sky_files, master_sci_files = find_sky(sci)
	masterSkies = []
	for object in master_sky_files:
		# Loop through each 2-d list of lists of sky files which correspond to an object.
		masterSkyGroup = []
		for group in object:
			# Loop over each list of sky files in the current group
			data_array = []
			for file in group:
				# Add all of the data from each file in the group to a list
				img = fits.open(file)
				data_array.append(img[0].data)
				img.close()
			# Median combine the sky files, outputting to a directory
			data_array = np.array(data_array)
			med = np.median(data_array, axis=0)
			hdu = fits.open(group[-1])
			hdu[0].data = med
			# Write information to the header of the new master sky about its creation
			fname = 'calibrations/Auto_Reduced/master_skies/' + date + '_' + group[-1].split('/')[-1][:-5] + '_master_sky.fits'
			hdu[0].header['HISTORY'] = '##########################'
			hdu[0].header['HISTORY'] = 'Generated master sky by median combining the following: '
			hdu[0].header['HISTORY'] = ', '.join(group)
			hdu[0].header['HISTORY'] = '##########################'
			hdu.writeto(fname, overwrite=True)
			# Create and write to a file with a list of the files that when into making this master sky
			f = open(fname[:-5] + '_files.list', 'w+')
			f.write('\n'.join(group))
			f.close()
			# Append this master sky to the list which will become part of masterSkies
			masterSkyGroup.append(fname)
		# Append the list of master skies for an object to masterSkies
		masterSkies.append(masterSkyGroup)
	return masterSkies, master_sci_files

def get_from_darkdb(raw_file):
	'''
	Retrieve a master dark and hpmap from the database. Uses the magnitude of distance
	in time and exposure time to find the most suitable dark.

	Params:
	- raw_file: The raw file to be calibrated with the master dark.

	Return:
	- masterDark: The closest master dark
	- hp_map: The corresponding hot pixel map
	'''
 	# Establish database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute('USE WIRC_POL')

	masterDark = ''
	hp_map = ''

	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"master_darks\"')
	if cursor.fetchone()[0] > 0:
		cursor.execute('SELECT File_Path, HP_MAP, UTSHUT, EXPTIME FROM master_darks')
		files = cursor.fetchall()
		if len(files) > 0:
			# Retreive the shutter times in modified julian form, for comparison
			# Also retrieve the exposure times
			time_0 = Time([fits.getheader(raw_file)['UTSHUT']])
			time_0 = time_0.mjd[0]
			exp_0 = fits.getheader(raw_file)['EXPTIME']
			times = [x[2] for x in files]
			times = Time(times)
			times = times.mjd
			exps = [float(x[3]) for x in files]

			# Create the magnitude metric to be used in finding the best master dark
			diff = []
			for i in range(len(times)):
				diff.append((times[i] - time_0)**2 + (exps[i] - exp_0)**2)
			diff = np.array(diff)

			ind = np.where(diff == min(diff))[0][0]
			connection.commit()
			connection.close()
			# Gather the filenpaths
			masterDark = files[ind][0]
			hp_map = files[ind][1]

	return masterDark, hp_map

def get_from_flatdb(raw_file, mask=False):
	'''
	Retrieve a master flat and bpmap from the database. Uses the difference in time
	to find the most suitable flat.

	Params:
	- raw_file: The file to be calibrated with the master flat
	- mask: Indicates whether or not the program is searching for a mask flat

	Return:
	- masterFlat: The closest masterFlat
	- bp_map: The corresponding bad pixel map
	'''
	# Establish database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute('USE WIRC_POL')

	masterFlat = ''
	bp_map = ''
	fore = fits.getheader(raw_file)['FORE']

	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"master_flats\"')
	if(cursor.fetchone()[0] > 0):
		cursor.execute('SELECT COUNT(*) from master_flats where FORE = \"PG\"')
		if (not mask) and fore == 'PG' and cursor.fetchone()[0] > 0:
				cursor.execute('SELECT File_Path, BP_MAP, UTSHUT FROM master_flats WHERE FORE = \"PG\"')
		else:
			cursor.execute('SELECT File_Path, BP_MAP, UTSHUT FROM master_flats WHERE NOT FORE = \"PG\"')
		files = cursor.fetchall()
		if len(files) > 0:
			# Retrieve the time in modified julian form for comparison
			time_0 = Time([fits.getheader(raw_file)['UTSHUT']])
			time_0 = time_0.mjd[0]

			# If finding a mask flat, attempt to identify all of the mask flats, removing anything else
			# If there are none, return empty strings
			if mask:
				files_temp = []
				for file in files:
					hdu = fits.open(file[0])
					header = hdu[0].header
					try:
						if 'OUT' in header['MASKPOS']:
							files_temp.append(file)
					except KeyError:
						pass
					hdu.close()
				if files_temp == []:
					return '', ''
				else:
					files = files_temp

			# Identify the times in modified julian form for comparison
			# When attempting to match by filters as well, program was too often returning no results. Switched to only time
			times = [x[2] for x in files]
			times = Time(times)
			times = times.mjd

			# Create list of differences in time
			diff = []
			for time in times:
				diff.append(abs(float(time) - float(time_0)))
			diff = np.array(diff)

			# Identify the closest master flat in time
			ind = np.where(diff == min(diff))[0][0]
			connection.commit()
			connection.close()

			# Retrieve the filepaths
			masterFlat = files[ind][0]
			bp_map = files[ind][1]

	return masterFlat, bp_map

def get_from_skydb(calibfile):
	'''
	Retrieve a master sky from the database. Uses the difference in time
	to find the most suitable sky.

	Params:
	- calibfile: The file to be matched with the master sky

	Return:
	- masterSky: The most suitable master sky
	'''
	# Establish database connection
	connection = sql.MySQLConnection()
	connection.connect(buffered=True, host=host, port=port, user=user, passwd=passwd)
	cursor = connection.cursor()
	cursor.execute('USE WIRC_POL')

	masterSky = ''

	cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"master_skies\"')
	if(cursor.fetchone()[0] > 0):
		cursor.execute('SELECT File_Path, UTSHUT FROM master_skies')
		files = cursor.fetchall()
		if len(files) > 0:
			# Retrieve shutter times in modified julian form for comparison
			time_0 = Time([fits.getheader(calibfile)['UTSHUT']])
			time_0 = time_0.mjd[0]
			times = [x[1] for x in files]
			times = Time(times)
			times = times.mjd

			# Generate list of time differences
			diff = []
			for time in times:
				diff.append(abs(float(time) - float(time_0)))
			diff = np.array(diff)

			# Identify the closest master sky
			ind = np.where(diff == min(diff))[0][0]
			connection.commit()
			connection.close()

			# Retrieve the filepath
			masterSky = files[ind][0]
	return masterSky

def closest_dark_hp(fname, masterDarks, HPMap):
	'''
	Finds the most suitable master dark and hp map to use for a given raw file.
	Will search the masterDarks list of generated darks if there are any. Otherwise,
	it will query the database and fall back on user input if nothing is found.

	Params:
	- fname: The file to be matched with a master dark
	- masterDarks: The list of master darks generated by pipeline (can be empty)
	- HPMap: The list of corresponding hot pixel maps (can also be empty)

	Return:
	- masterDark: The most suitable master dark for the passed file
	- hp_map: The corresponding hot pixel map
	'''
	if len(masterDarks) > 0:
		# Identify the shutter and exposure times from the fits files
		FMT = '%H:%M:%S.%f'
		raw_time = datetime.strptime(fits.getheader(fname)['UTSHUT'][11:], FMT)
		raw_exp = fits.getheader(fname)['exptime']
		times = np.array([datetime.strptime(fits.getheader(x)['UTSHUT'][11:], FMT) for x in masterDarks])
		exps = np.array([fits.getheader(x)['exptime'] for x in masterDarks])
		# Generate list of distance metric
		dist = []
		for i in range(len(times)):
			dist.append(np.sqrt((times[i] - raw_time).total_seconds()**2 + (exps[i] - raw_exp)**2))
		dist = np.array(dist)
		# Identify closest master dark
		ind = np.where(dist == min(dist))[0][0]
		return masterDarks[ind], HPMap[ind]
	else:
		# If there are no masterDarks (either no dark files or command line argument says to use existing)
		# Search database for master dark
		masterDark, hp_map = get_from_darkdb(fname)
		# If the query was unsuccessful, rely on user input
		if masterDark == '' or hp_map == '':
			while True:
				# Loops until valid files are entered
				try:
					masterDark = raw_input('No master dark was found. Enter one: ')
					hp_map = raw_input('Enter the corresponding HPMap: ')
					# Verify file validity
					x = fits.open(masterDark)
					y = fits.open(hp_map)
					x.close()
					y.close()
					break
				except IOError:
					print('Invalid file(s) entered!\n')
					continue
		return masterDark, hp_map

def closest_flat_bp(fname, masterFlats, BPMap):
	'''
	Finds the most suitable master flat and bp map to use for a given raw file.
	Will search the masterFlats list of generated flats if there are any. Otherwise,
	it will query the database and fall back on user input if nothing is found.

	Params:
	- fname: The file to be matched with a master flat
	- masterFlats: The list of master flats generated by the pipeline (can be empty)
	- BPMap: The list of corresponding master flats (can also be empty)
	'''
	if len(masterFlats) > 0:
		# Identify the fore filters and shutter times from the fits files
		FMT = '%H:%M:%S.%f'
		fore = fits.getheader(fname)['FORE']
		fores = [fits.getheader(x)['FORE'] for x in masterFlats]
		raw_time = datetime.strptime(fits.getheader(fname)['UTSHUT'][11:], FMT)
		# Gather times from the appropriate subset of files
		if fore == 'PG' and 'PG' in fores:
			# If the file is a PG image and there exists a PG flat
			times = np.array([(i, datetime.strptime(fits.getheader(masterFlats[i])['UTSHUT'][11:], FMT)) for i in range(len(masterFlats))
					if fores[i] == 'PG'])
		else:
			times = np.array([(i, datetime.strptime(fits.getheader(masterFlats[i])['UTSHUT'][11:], FMT)) for i in range(len(masterFlats))
					if fores[i] != 'PG'])
		# Generate the list of time differences
		dist = []
		for i in range(len(times)):
			dist.append(abs((times[i][1] - raw_time).total_seconds()))
		dist = np.array(dist)
		# Identify the closest master flat
		ind = np.where(dist == min(dist))[0][0]
		return masterFlats[times[ind][0]], BPMap[times[ind][0]]
	else:
		# If no flats were found or use_existing keyword is active
		# Query database for master flat and bp map
		masterFlat, bp_map = get_from_flatdb(fname)
		# If query is unsuccessful
		if masterFlat == '' or bp_map == '':
			while True:
				# Loop until valid files are entered
				try:
					masterFlat = raw_input('No master flat was found. Enter one: ')
					bp_map = raw_input('Enter the corresponding BPMap: ')
					# Check file validity
					x = fits.open(masterFlat)
					y = fits.open(bp_map)
					x.close()
					y.close()
					break
				except IOError:
					print('Invalid file(s) entered!\n')
					continue
		return masterFlat, bp_map

def closest_sky(calib_obj, masterSkies, master_sci_files):
	'''
	Identifies the most suitable sky image (from those available) to use for a
	specific calibrated file. Queries database if none were generated., then falls
	back on user input.

	Params:
	- calib_obj: The calibrated wirc_data object to be updated with a master sky
	- masterSkies: The 2-d list of all master sky files, grouped by object
	- master_sci_files: The parallel 2-d list of all science files, grouped by object
	'''
	empty = True
	for sky in masterSkies:
		if len(sky) > 0:
			empty = False
			break

	if not empty:
		# Identify the appropriate list of master skies to use when finding the closest sky
		# Looks for file name in master_sci_files (parallel list)
		sky_ind = -1
		for i in range(len(masterSkies)):
			if calib_obj.header['CAL_FN'] in master_sci_files[i]:
				sky_ind = i
				break
		# If there was no list found for this file, return (indicates that the file passed is a sky file)
		if sky_ind < 0:
			return
		# print('############## Testing Sky for {}##############'.format(calib_obj.header['CAL_FN']))
		# print(masterSkies)
		# print(masterSkies[sky_ind])
		# print(master_sci_files[sky_ind])

		# If the list associated with a calib_obj is empty, place 'None' in the header
		if masterSkies[sky_ind] == []:
			calib_obj.header['SKY_FN'] = 'None'
			return

		# Gather the barycentric julian dates from the fits headers
		time_0 = float(calib_obj.header['BJD'])
		times = [fits.getheader(x)['BJD'] for x in masterSkies[sky_ind]]

		# Calculate list of time differences
		diff = []
		for time in times:
			diff.append(abs(time - time_0))
		diff = np.array(diff)

		# Identify appropriate master sky and place it in the header of the calibrated file
		calib_obj.sky_fn = masterSkies[sky_ind][np.where(diff == min(diff))[0][0]]
		calib_obj.header['SKY_FN'] = calib_obj.sky_fn
	else:
		# If no skies were generated
		# Query database for master sky
		calib_obj.sky_fn = get_from_skydb(calib_obj.header['CAL_FN'])
		if calib_obj.sky_fn == '':
			while True:
				# Loop until valid file is given
				try:
					calib_obj.sky_fn = raw_input('No master sky was found. Enter one: ')
					# Verify file validity
					x = fits.open(calib_obj.sky_fn)
					x.close()
					break
				except IOError:
					print('Invalid file(s) entered!\n')
					continue
		# Write filename to calibrated object
		calib_obj.header['SKY_FN'] = calib_obj.sky_fn

def get_calib_files(fnames, types, date, use_existing=False, no_db=False):
	'''
	Goes through the process of generating or finding the darks and flats to be
	used for calibration.

	Params:
	- fnames: The files to generate or find calibrations for
	- types: The parallel list of image types corresponding to files
	- use_existing: The flag to use the database instead of generating
	- no_db: The flag to not enter any files into the database

	Return:
	- files: A list of dictionaries containing filepaths and matched calibrations:
		[{'RAW':'YYYYMMDD/image0123.fits', 'DARK':'filepath', 'FLAT':'filepath',
			'BP':'filepath', 'HP':'filepath'}, {...}, ...]
	'''
	# Commented out in case someone else wants it, but was inferior to current method
	# date = fnames[0].split('/')[0]
	# if use_existing:
	# 	masterDarks, HPMap = get_from_darkdb(date)
	# 	masterFlats, BPMap = get_from_flat_db(date)
	# 	if len(masterDarks) == 0:
	# 		while True:
	# 			try:
	# 				masterDark = raw_input('No master dark was found. Enter one: ')
	# 				HP = raw_input('Enter the corresponding HPMap: ')
	# 				x = fits.open(masterDark)
	# 				y = fits.open(HP)
	# 				x.close()
	# 				y.close()
	# 				masterDarks = [masterDark]
	# 				HPMap = [HP]
	# 				break
	# 			except IOError:
	# 				print('Invalid file(s) entered!\n')
	# 				continue
	# 	if len(masterFlats) == 0:
	# 		while True:
	# 			try:
	# 				masterFlat = raw_input('No master flat was found. Enter one: ')
	# 				BP = raw_input('Enter the corresponding BPMap: ')
	# 				x = fits.open(masterFlat)
	# 				y = fits.open(BP)
	# 				x.close()
	# 				y.close()
	# 				masterFlats = [masterFlat]
	# 				BPMap = [BP]
	# 				break
	# 			except IOError:
	# 				print('Invalid file(s) entered!\n')
	# 				continue
	# else:
	# date = fnames[0].split('/')[0]

	darks, flats, sci = split_by_type(fnames, types)
	masterDarks = []
	masterFlats = []
	HPMap = []
	BPMap = []
	# If there are no science images, print an error and write it to the log
	if len(sci) == 0:
		f = open('autoreduction_logs/Errors.log', 'a+')
		print('No science images found.')
		f.write(str(datetime.now()) + ' - No science images found in {}\n'.format(date))
		quit()
	# If there are darks and the user wants the calibrations to be generated
	if len(darks) > 0 and not use_existing:
		# Create the folder for auto reduced master darks
		path = 'calibrations/Auto_Reduced/master_darks/'
		if not os.path.exists(path):
			os.makedirs(path)
		masterDarks, HPMap, master_dark_files = generate_darks(darks, date)
		print('CREATED MASTER DARKS')
		# If the user is allowing database storage, store the generated darks
		if not no_db:
			load_db.new_darks(masterDarks, HPMap)
	# If there are flats and the user wants the calibrations to be generated
	if len(flats) > 0 and not use_existing:
		# Create the folder for auto reduced master flats
		path = 'calibrations/Auto_Reduced/master_flats/'
		if not os.path.exists(path):
			os.makedirs(path)
		masterFlats, BPMap, master_flat_files = generate_flats(flats, date, masterDarks, HPMap)
		print('CREATED MASTER FLATS')
		# If the user is allowing database storage, store the generate flats
		if not no_db:
			load_db.new_flats(masterFlats, BPMap)

	# Use a list of dictionaries to store the darks, flats, bps, and hps matched with each raw file
	files = []
	for fname in sci:
		file_dict = {}
		dark = ''
		flat = ''
		bp = ''
		hp = ''
		file_dict['RAW'] = fname
		dark, hp = closest_dark_hp(fname, masterDarks, HPMap)
		flat, bp = closest_flat_bp(fname, masterFlats, BPMap)
		file_dict['DARK'] = dark
		file_dict['FLAT'] = flat
		file_dict['BP'] = bp
		file_dict['HP'] = hp
		files.append(file_dict)

	return files

def do_calibration(files, date, use_existing=False, no_db=False):
	'''
	Calibrate the given files, using a passed in dictionary of files and their
	calibrations.

	Params:
	- files: Dictionary containing raw file names, bp, hp, dark, flat:
		[{'RAW':'YYYYMMDD/image0123.fits', 'DARK':'filepath', 'FLAT':'filepath',
			'BP':'filepath', 'HP':'filepath'}, {...}, ...]
	- date: The night for which images are being calibrated
	- use_existing: Command line argument indicating whether or not to generate
					calibrations (used for skies)
	- no_db: Command line argument indicating whether or not to store in database
			 (used for skies)

	Return:
	- calib_objs: A list of calibrated wirc_data objects
	'''
	if len(files) == 0:
		return []
	# Create the appropriate directory for Calibrated Files
	file_path = 'Calibrated Files/' + files[0]['RAW'][:8] + '/Auto_Reduced/'
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	calib_file_dicts = []
	calib_objs = []
	calib_files = []
	for file in files:
		# Create a wirc object
		data = wo.wirc_data(raw_filename=file['RAW'], dark_fn=file['DARK'], \
			flat_fn=file['FLAT'], bp_fn=file['BP'], hp_fn=file['HP'])
		data.calibrate()
		# Save the calibrated wirc object
		filename = file_path + file['RAW'].split('/')[1][:-5] + '_cal.fits'
		data.header['CAL_FN'] = filename
		data.save_wirc_object(filename)
		calib_files.append(filename)
		calib_objs.append(data)
	masterSkies = []
	master_sci_files = []
	# If user wants new calibrations to be created, generate master skies
	if not use_existing:
		# Create appropriate filepath for auto reduced master skies
		path = 'calibrations/Auto_Reduced/master_skies/'
		if not os.path.exists(path):
			os.makedirs(path)
		masterSkies, master_sci_files = generate_sky(calib_files, date)
		# If user is allowing database uploads, upload skies to database
		if not no_db:
			for sky_list in masterSkies:
				load_db.new_skies(sky_list)
	# Match each calibrated object with a master sky
	for obj in calib_objs:
		closest_sky(obj, masterSkies, master_sci_files)
		obj.save_wirc_object(obj.header['CAL_FN'])

	return calib_objs
