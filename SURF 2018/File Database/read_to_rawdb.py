import sys, glob, load_db, create_darks_flats
from load_db import new_raw_entry, new_calib_entry, gen_types
from create_darks_flats import do_calibration, get_calib_files
from sources import process_sources
from datetime import datetime
import git
import os

data_dir = # Removed for security reasons #
repo_dir = # Removed for security reasons #

def print_usage(verbose=False):
	'''
	Print the usage message to the terminal.
	'''
	if not verbose:
		print('USAGE: $python read_to_rawdb.py YYYYMMDD [options]')
	else:
		print('\nUSAGE: $python read_to_rawdb.py YYYYMMDD [options]\n\n'

		'-f file1 [file2 ...]  : Reduce the specific files listed after the -f argument (Give calibrated files if processing sources)\n'

		'-u                    : Reduce using database files, not by generating calibrations\n'

		'-s 				   : Only process sources, then quit the program\n'

		'--nodb                : Do not upload any files to the database during the reduction process\n'

		'--raw 				   : Only handle raw files, then quit the program\n'

		'--cals                : Generate calibrations but do not continue the reduction process\n'

		'--nosrc			   : Do not process the sources and complete reduction\n'

		'--help                : Print help string\n')

def data_reduction(files, date, use_existing=False, calibrate=True, no_db=False, raw=False, sources=False, files_given=False, no_srcs=False):
	'''
	This function administers the data reduction process, calling the functions in
	associated files to perform it.

	Params:
	- files: The files to be reduced.
	- date: The night for which files are being reduced.
	- use_existing: Flag to use the calibrations in the database, rather than generate.
	- calibrate: Flag to calibrate the files, not just generate calibrations.
	- no_db: Flag to refrain from entering files into the database during reduction.
	- raw: Flag to only upload raw files and quit.
	- sources: Flag to find and process sources then quit
	- files_given: Flag indicating whether files were given or only a date (Filenames follow -f)
	- no_srcs: Flag indicating whether or not the user wants to find and process sources
	'''
	files.sort()
	f = open('autoreduction_logs/Activity.log', 'a+')
	# Print Information to log
	repo = git.Repo(repo_dir)
	sha = repo.head.object.hexsha
	if files_given:
		f.write('------ Pipeline Version: ' + str(sha) + ' - ' + str(datetime.now()) + ' - Reducing ' + ', '.join(files) + ' ------\n')
	else:
		f.write('------ Pipeline Version: ' + str(sha) + ' - ' + str(datetime.now()) + ' - Reducing ' + files[0].split('/')[0] + ' ------\n')
	if sources:
		# If the sources keyword is activated, process sources and quit
		if not files_given:
			files = []
		f.write(str(datetime.now()) + ' - Beginning Source Processing\n')
		process_sources(files, date=date, sources=sources)
		f.write(str(datetime.now()) + ' - Finished Source Processing\n')
		quit()
	# Identify the raw file types
	types = gen_types(files)
	if not no_db and calibrate:
		# If the no_db keyword is not activated and the user is not only seeking to generate calibrations
		f.write(str(datetime.now()) + ' - Uploading Raw Files to Database\n')
		new_raw_entry(files, types)
		f.write(str(datetime.now()) + ' - Finished Uploading Raw Files to Database\n')
		if raw:
			quit()
	# Generate the calibrations (or match them if attempting to use existing)
	f.write(str(datetime.now()) + ' - Generating/Retrieving Calibrations\n')
	if not calibrate:
		# Allows the user to enter specific files to generate calibrations, if desired
		use_existing = False
	file_cal_dict = get_calib_files(files, types, date, use_existing=use_existing, no_db=no_db)
	f.write(str(datetime.now()) + ' - Finished Generating/Retrieving Calibrations')
	if calibrate:
		# This if statement controls when a user just wants to generate calibrations and stop
		f.write(str(datetime.now()) + ' - Beginning Calibration\n')
		calib_objs = do_calibration(file_cal_dict, date, use_existing=use_existing, no_db=no_db)
		f.write(str(datetime.now()) + ' - Finished Calibration\n')
		if not no_db:
			# If the user has elected to use the database
			f.write(str(datetime.now()) + ' - Uploading Calibrated Files to Database\n')
			new_calib_entry(calib_objs)
			f.write(str(datetime.now()) + ' - Finished Uploading Calibrated Files to Database\n')

		if not no_srcs:
			# If the user has elected not to process sources
			f.write(str(datetime.now()) + ' - Beginning Source Processing\n')
			process_sources(calib_objs, date=date)
			f.write(str(datetime.now()) + ' - Finished Source Processing\n')

		# Still need to write code to store source information in the database
		f.write('------ ' + str(datetime.now()) + ' Finished Reduction ------\n')
		f.close()

if __name__ == '__main__':
	# Handle command line arguments
	files_given = False
	use_existing = False
	calibrate = True
	no_srcs = False
	no_db = False
	raw = False
	sources = False
	if '--help' in sys.argv:
		# Argument to print the usage message
		print_usage(verbose=True)
		quit()
	if '-f' in sys.argv:
		# Argument indicating files passed
		files_given = True
	if '-u' in sys.argv:
		# Argument to use existing calibrations in database
		use_existing = True
		sys.argv.remove('-u')
	if '--cals' in sys.argv:
		# Argument to generate calibrations then stop
		calibrate = False
		sys.argv.remove('--cals')
	if '--nosrc' in sys.argv:
		# Argument to not process sources
		no_srcs = True
		sys.argv.remove('--nosrc')
	if '--nodb' in sys.argv:
		# Argument to avoid uploading the database
		no_db = True
		sys.argv.remove('--nodb')
	if '--raw' in sys.argv:
		# Argument to upload raw files to the database then stop
		raw = True
		sys.argv.remove('--raw')
	if '-s' in sys.argv:
		# Argument to process sources in given files (or calibrated directory) then stop
		sources = True
		sys.argv.remove('-s')
	# Ensure the directory in use is correct (needed for riri)
	os.chdir(data_dir)
	if len(sys.argv) == 1  or (len(sys.argv) < 4 and '-f' in sys.argv) or \
	sys.argv[1][0] == '-':
		# If there is some sort of error in the command line call
		print_usage()
	elif len(sys.argv) == 2:
		date = sys.argv[1]
		if glob.glob(date) == []:
			print('ERROR: Directory does not exist!')
		else:
			# Get all files in the directory which match the appropriate pattern for images.
			files = list(glob.glob(date + '/*[0-9][0-9][0-9][0-9].fits'))
			files += list(glob.glob(date + '/*[0-9][0-9][0-9][0-9]-[0-9].fits'))
			# Execute the data reduction process
			data_reduction(files, date, use_existing=use_existing, calibrate=calibrate, \
						no_db=no_db, raw=raw, sources=sources, files_given=files_given, no_srcs=no_srcs)
	elif len(sys.argv) == 3:
		# Some sort of error
		print_usage()
	elif len(sys.argv) >= 4:
		date = sys.argv[1]
		# Takes all of the files entered after the -f flag.
		files = sys.argv[sys.argv.index('-f') + 1:]
		files = [date + '/' + x for x in files]
		# Execute the data reduction process
		data_reduction(files, date, use_existing=True, calibrate=calibrate, no_db=no_db, \
		 			raw=raw, sources=sources, files_given=files_given, no_srcs=no_srcs)
