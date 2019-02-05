# NEEDS TO BE UPDATED. JUST A PLACEHOLDER


Dependencies:

$conda install flask
$conda install wtforms
$conda install pathlib


Running locally:

To run the website locally, you need to first open an ssh tunnel in order to access the
database from riri, then modify the website code slightly to accommodate the different port
needed for ssh tunneling.

1. Clone the WIRC-Pol-Website repository

2. Go to the terminal and run the following:
   $ssh -L 3307:localhost:3306 user@riri.caltech.edu -N

3. Edit WIRC-Pol-Website/flask/app/views.py line 20:
   port_conn=3306 -> port_conn=3307

4. Open a new terminal window and navigate to WIRC-Pol-Website/flask/ and run:
   $python run.py

5. Enter a browser and navigate to localhost:5000


# Use

/search
> The query page for narrowing down your brown dwarf target possibilities.
> Returns a table of targets which can be clicked to take you to individual target pages.

/targets
> The page to view and query all of the targets in the database.

/<target>
> All information available on a given target and a finding chart.

/fc
> Takes an object name, RA and Dec and gives back a finding chart for that object.

/standards
> A table of standard stars.

/references
> A table of reference papers for the information on each target.
