# File-Database

PLEASE READ IN FULL

This repository contains the code for the automated data reduction pipeline. The README contains
helpful information on how to use the automated pipeline, including example commands for various
situations.

In DB Setup:
The config_db.py file has the code to do the initial setup of the database. Make sure the master_BD.csv, target_refs.csv and standards.csv files are
in the same directory as config_db.py and that the user information is appropriate in the connection in the
config_db.py file. Run this at a terminal, assuming you have a working MySQL server, and it should configure
the targets table, which is all that is necessary for much of the other code to be testable.


Requirements:
Python (written for 2.7)
astropy
numpy
wirc_drp (as well as the WIRC_DRP environment variable)
working MySQL server with WIRC_POL database

Usage:
USAGE: $python read_to_rawdb.py YYYYMMDD [options]

-f file1 [file2 ...]  : Reduce the specific files listed after the -f argument (Give calibrated files if processing sources)

-u                    : Reduce using database files, not by generating calibrations

-s 				            : Only process sources, then quit the program

--nodb                : Do not upload any files to the database during the reduction process

--raw 				        : Only handle raw files, then quit the program

--cals                : Generate calibrations but do not continue the reduction process (skips raw_files upload)

--nosrc			          : Do not process the sources and complete reduction

--help                : Print help string


Example Uses:
- Plain reduction from start to finish on directory /scr/data/20180621:
  $python read_to_rawdb.py 20180621

- Create calibrations for directory /scr/data/20180621:
  $python read_to_rawdb.py 20180621 --cals

- Calibrate specific files from /scr/data/20180621, using existing calibrations
  (-u is automatically applied along with -f)
  $python read_to_rawdb.py 20180621 --nosrc -f image0001.fits image0007.fits image0020.fits

- Process sources for /scr/data/20180621:
  $python read_to_rawdb.py 20180621 -s

- Reduce specific files in /scr/data/20180621, using existing calibrations, without uploading to database:
  (-u is automatically applied along with -f)
  $python read_to_rawdb.py 20180621 -f image0009.fits image0200.fits --nodb

- Generate calibrations from specific files in /scr/data/20180621:
  (-u will be deactivated when -f is paired with --cals)
  $python read_to_rawdb.py 20180621 --cals -f image0250.fits image0003.fits image0100.fits

- Upload only specific raw files to the database from /scr/data/20180621:
  $python read_to_rawdb.py 20180621 --raw -f image0050.fits image0037.fits
