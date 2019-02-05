# imports
from flask import render_template, request, redirect, flash, send_file, session
from mysql import connector as sql
from app import app
from forms import QueriesForm, FindingForm
from collections import OrderedDict
import maskDraw
from pathlib import Path
import matplotlib
# Ensures that no plots will be generated and displayed unnecessarily
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
from io import BytesIO
from auth import login_required
import socket


# define global variables
form = QueriesForm()
num = 1
host_conn = 'localhost'
# Check whether the website is running online or locally to identify the appropriate database port
hostname = socket.gethostname()
if hostname == 'riri':
    port_conn = 3306
else:
    port_conn = 3307

# Database connection variables
user_conn = # Removed for security reasons #
passwd_conn = # Removed for security reasons #
db_conn = 'WIRC_POL'

db = sql.MySQLConnection()
cursor = None
root_dir = # Removed for security reasons #

def reconnect():
    '''
    Regenerates the database connection to ensure the most current data is
    displayed on the website.
    '''
    global cursor
    db.close()
    db.connect(host=host_conn, port=port_conn, user=user_conn, passwd=passwd_conn, db=db_conn)
    cursor = db.cursor()

def search_db(query):
    '''
    Takes a query and returns search results in the form of a table with user-
    defined columns.

    Params:
    - query: A string containing an SQL query.

    Return:
    - A 2-d list with each row corresponding to a row of query results
    '''
    reconnect()
    cursor.execute(query)
    stars = cursor.fetchall()
    # Put the data in a 2-d list to make it easier to work with
    all_data = []
    for star in stars:
        data = []
        for x in range(0, len(star)):
            data.append(star[x])
        all_data.append(data)
    db.close()
    return all_data

def build_search_query(num):
    '''
    This function uses input from the search interface on the website in order to
    generate an SQL query appropriately.

    Params:
    - num: The number of query parameters used in searching

    Return:
    - The formatted query string
    '''
    # Gather column names from those entered by the user
    query_str = 'SELECT `' + '`, `'.join(request.form['view'].replace(', ', ',').split(',')) + '` FROM targets WHERE'
    # Generate the appropriate strings to put after WHERE in the sql query
    wheres = []
    for i in range(num):
        # Gather data from the search form
        field = '`' + request.form['queries-%d-field' %i] + '`'
        condition = request.form['queries-%d-condition' %i]
        query = request.form['queries-%d-query' %i]
        # Appropriately formats strings based on the given condition
        if condition == '>' or condition == '<':
            where = ' ' + field + ' ' + condition + ' ' + query + ' '
        elif condition == 'range':
            range_l = query.replace(', ', ',').split(',')
            where = ' ({0} < {1} AND {0} > {2}) '.format(field, range_l[1], range_l[0])
        elif condition == 'in':
            where = ' {0} LIKE \"%{1}%\" '.format(field, query)
        else:
            where = ' {0} = \"{1}\" '.format(field, query)
        wheres.append(where)
    if len(wheres) > 1:
        # Appends all of the where clauses to the query
        # Might be worth adding a checkbox on the website to switch between AND and OR (to get different subsets)
        query_str += 'OR'.join(wheres)
    else:
        # If there is only one, append it
        query_str += wheres[0]
    return query_str

### This function seemed to be more trouble than it was worth ###
# def format_query(query):
#     end_index = query.upper().index('FROM')
#     columns = query.strip()[6:end_index].strip().replace(', ', ',').replace('`', '')
#     query_front = query[0:6]
#     query_back =  query[end_index:]
#
#     columns = ' `' + '`, `'.join(columns.split(',')) + '` '
#
#     return query_front + columns + query_back

@app.route('/')
@login_required
def home():
    '''
    The main page.
    '''
    return render_template('home.html')

@app.route('/<path:path>')
#@login_required
def schemaspy(path):
    '''
    A sort of wrapper function which serves static files. (Needed for SchemaSpy)
    '''
    return app.send_static_file(path)

@app.route('/standards', methods=['GET', 'POST'])
@login_required
def standards():
    '''
    Create a webpage to hold a table of data from stars from the
    standards collection of the current database.
    '''
    # Define properties to show in table
    properties = ['stan_id', 'Target', 'RA', 'Dec', 'V', 'J', 'K', 'H', 'SpTy']
    # Collect data in lists
    all_data = search_db('SELECT * FROM standards')
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        properties = []
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather the appropriate data from the query
            data = search_db(query)
            for descriptor in cursor.description:
                properties.append(descriptor[0])
            return render_template('standards.html',
                           properties=properties,
                           data=data)
    # Render data in a table with template standards.html
    return render_template('standards.html',
                           properties=properties,
                           data=all_data)

@app.route('/references', methods=['GET', 'POST'])
@login_required
def references():
    '''
    Create a webpage to hold a table of data from stars from the
    standards collection of the current database.
    '''
    # Gather the column names from the target_refs table
    all_data = search_db('SELECT * FROM target_refs')
    fields = []
    for field in cursor.description:
        fields.append(field[0])
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather the appropriate data from the query
            data = search_db(query)
            fields = []
            for field in cursor.description:
                fields.append(field[0])
            return render_template('ref.html',
                           fields=fields,
                           data=data)
    # Render data in a table with template ref.html
    return render_template('ref.html',
                           fields=fields,
                           data=all_data)

def url_safe(name):
    '''
    Replace appropriate characters in a string to make it an appropriate URL.
    '''
    # It is unclear if these are sufficient
    #url_safe_name = name.replace('+', '_')
    #url_safe_name = name.replace('-', '_')
    url_safe_name = name.replace(' ', '_')
    url_safe_name = name.replace('/', '-')
    return url_safe_name

@app.route('/query_db', methods=['GET', 'POST'])
@login_required
def query_db():
    '''
    Create the webpage which queries the database and displays the results
    in a table.
    '''
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather data from the database
            fields = []
            names = []
            data = search_db(query)
            for field in cursor.description:
                fields.append(field[0])
            # If the Name column is there, move it to the front (for finding charts)
            if(u'Name' in fields):
                name_ind = fields.index(u'Name')
                fields.remove(u'Name')
                fields.insert(0, u'Name')
                for i in range(0, len(data)):
                    temp = data[i][name_ind]
                    data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                    names.append(url_safe(data[i][0]))
            return render_template('query.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=len(data),
                           count=len(data))
    return render_template('query.html', fields=[], names=[], data=[], length=0, count=0)

@app.route('/targets', methods=['GET', 'POST'])
@login_required
def targets():
    '''
    Create a webpage to hold a table of data from various stars from the
    targets collection of the current database, with the option to change
    the number of targets viewable on the page.
    '''
    # If the user has submitted a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather data from the database
            fields = []
            names = []
            data = search_db(query)
            for field in cursor.description:
                fields.append(field[0])
            # If the Name column is present, move it to the front for finding chart links
            if(u'Name' in fields):
                name_ind = fields.index(u'Name')
                fields.remove(u'Name')
                fields.insert(0, u'Name')
                for i in range(0, len(data)):
                    temp = data[i][name_ind]
                    data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                    names.append(url_safe(data[i][0]))
            return render_template('targets.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=len(data),
                           count=len(data))
    # Define the collection that data will be pulled from
    all_data = search_db('SELECT `Name`, `RA`, `DEC`, `SpT`, `Peculiarities`, `J` FROM targets LIMIT 100')

    # Define properties to show in table
    fields = ['Name', 'RA', 'DEC', 'SpT',' Peculiarities', 'J']

    names = []
    for star in all_data:
        names.append(url_safe(star[0]))

    length = len(all_data)
    return render_template('targets.html',
                           fields=fields,
                           names=names,
                           data=all_data,
                           length=length,
                           count=length)



@app.route('/target/<url_safe_name>')
@login_required
def target(url_safe_name):
    '''
    Creates a table of all information on a given target as well as a finding
    chart.
    '''
    # Put target name into SQL search format
    pattern = url_safe_name.replace('_', '%')
    # Search database for target and make lists of characteristics
    properties = search_db('SELECT * FROM targets')
    fields = []
    for field in cursor.description:
        fields.append(field[0])

    target = search_db('SELECT * FROM targets WHERE `Name` LIKE \"' + pattern + "\"")
    # Append the gathered information into a list, placing Name first
    items = []
    for i in range(0, len(fields)):
        if fields[i] == u'Name':
            items.insert(0, (fields[i], target[0][i]))
        else:
            items.append((fields[i], target[0][i]))

    # Query for variables used in finding chart generation
    fc_vars = search_db('SELECT `Name`, `RA`, `DEC` FROM targets WHERE `Name` LIKE \"' + pattern + "\"")

    var_list = []
    for var in fc_vars[0]:
        var_list.append(var)

    name, ra, dec = var_list
    # Create the filename to save/search for the finding chart
    fname = '/img/'+name.replace(' ', '_')+'_'+'finding_chart_'+ str(ra)+'_'+str(dec)+'J'+'.png'
    file = Path('app/static' + fname)
    # If the finding chart does not exist, create it
    if(not file.exists()):
        # Draw and save finding chart
        maskDraw.findingChart(float(ra), float(dec), 'J',  14.5,
                                target_name = name,
                                output_prefix='app/static/img/'+name.replace(' ', '_')+'_')

    # Render table and finding chart
    return render_template('object.html',
                            items=items,
                            fname=fname,
                            )

@app.route('/rawfiles', methods = ['GET', 'POST'])
@login_required
def rawfiles():
    '''
    This page displays the database information related to the raw_files table.
    '''
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather database information
            fields = []
            names = []
            data = search_db(query)
            for field in cursor.description:
                fields.append(field[0])
            # Move File_Path to the front for fitsview links
            if(u'File_Path' in fields):
                name_ind = fields.index(u'File_Path')
                fields.remove(u'File_Path')
                fields.insert(0, u'File_Path')
                for i in range(0, len(data)):
                    temp = data[i][name_ind]
                    data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                    # data[i].insert(0, temp)
                    names.append(url_safe(data[i][0]))
            return render_template('rawfiles.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=len(data),
                           count=len(data))
    # Define the collection that data will be pulled from
    all_data = search_db('SELECT * FROM raw_files LIMIT 100')

    # Define properties to show in table
    # This process is so involved because it ensures that File_Path will be first,
    # as needed for fitsview links
    fields = list(cursor.column_names)
    fields = fields[1:2] + fields[0:1] + fields[2:]
    names = []
    data = []
    for file in all_data:
        names.append(url_safe(file[1]))
        data.append(file[1:2] + file[0:1] + file[2:])

    length = len(all_data)
    return render_template('rawfiles.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=length,
                           count=length)

@app.route('/calibfiles', methods = ['GET', 'POST'])
@login_required
def calibfiles(n_entries = 100):
    '''
    This page displays database information from calib_files.
    '''
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather information from the database
            fields = []
            names = []
            data = search_db(query)
            for field in cursor.description:
                fields.append(field[0])
            # Move File_Path to the front for the fitsview links
            if(u'File_Path' in fields):
                name_ind = fields.index(u'File_Path')
                fields.remove(u'File_Path')
                fields.insert(0, u'File_Path')
                for i in range(0, len(data)):
                    temp = data[i][name_ind]
                    data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                    names.append(url_safe(data[i][0]))
            return render_template('calibfiles.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=len(data),
                           count=len(data),
                           query = query)

    interesting_fields = ["tar_id","File_Path","Raw_File", "UTSHUT","FORE","AFT","MASKPOS","EXPTIME","OBJECT"]
    query_fields = ",".join(interesting_fields)

    # Define the collection that data will be pulled from
    query = 'SELECT {} FROM calib_files LIMIT {}'.format(query_fields,n_entries)
    #query = 'SELECT * from calib_files LIMIT{}'.format(n_entries)
    all_data = search_db(query)

    # Define properties to show in table
    # It is so involved because it moves File_Path to the front
    fields = list(cursor.column_names)
    fields = fields[1:2] + fields[0:1] + fields[2:]
    names = []
    data = []
    for file in all_data:
        names.append(url_safe(file[1]))
        data.append(file[1:2] + file[0:1] + file[2:])

    length = len(all_data)
    return render_template('calibfiles.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=length,
                           count=length,
                           query = query)

@app.route('/darks', methods = ['GET', 'POST'])
@login_required
def darks():
    '''
    This page displays database information on the master_darks
    '''
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather information from the database
            fields = []
            names = []
            data = search_db(query)
            for field in cursor.description:
                fields.append(field[0])
            # Move File_Path to the front for fitsview
            if(u'File_Path' in fields):
                name_ind = fields.index(u'File_Path')
                fields.remove(u'File_Path')
                fields.insert(0, u'File_Path')
                for i in range(0, len(data)):
                    temp = data[i][name_ind]
                    data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                    names.append(url_safe(data[i][0]))
            return render_template('darks.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=len(data),
                           count=len(data))
    # Define the collection that data will be pulled from
    all_data = search_db('SELECT * FROM master_darks LIMIT 100')

    # Define properties to show in table
    fields = list(cursor.column_names)

    names = []
    for file in all_data:
        names.append(url_safe(file[0]))

    length = len(all_data)
    return render_template('darks.html',
                           fields=fields,
                           names=names,
                           data=all_data,
                           length=length,
                           count=length)

@app.route('/flats', methods = ['GET', 'POST'])
@login_required
def flats():
    '''
    This page shows database information from master_flats.
    '''
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather information from the database
            fields = []
            names = []
            data = search_db(query)
            for field in cursor.description:
                fields.append(field[0])
            # Move File_Path to the front for the fitsview links
            if(u'File_Path' in fields):
                name_ind = fields.index(u'File_Path')
                fields.remove(u'File_Path')
                fields.insert(0, u'File_Path')
                for i in range(0, len(data)):
                    temp = data[i][name_ind]
                    data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                    names.append(url_safe(data[i][0]))
            return render_template('flats.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=len(data),
                           count=len(data))
    # Define the collection that data will be pulled from
    all_data = search_db('SELECT * FROM master_flats LIMIT 100')

    # Define properties to show in table
    fields = list(cursor.column_names)

    names = []
    for file in all_data:
        names.append(url_safe(file[0]))

    length = len(all_data)
    return render_template('flats.html',
                           fields=fields,
                           names=names,
                           data=all_data,
                           length=length,
                           count=length)

@app.route('/skies', methods = ['GET', 'POST'])
@login_required
def skies():
    '''
    This webpage shows database information on master_skies
    '''
    # If the user has entered a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather information from the database
            fields = []
            names = []
            data = search_db(query)
            for field in cursor.description:
                fields.append(field[0])
            # Move File_Path to the front for fitsview links
            if(u'File_Path' in fields):
                name_ind = fields.index(u'File_Path')
                fields.remove(u'File_Path')
                fields.insert(0, u'File_Path')
                for i in range(0, len(data)):
                    temp = data[i][name_ind]
                    data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                    names.append(url_safe(data[i][0]))
            return render_template('skies.html',
                           fields=fields,
                           names=names,
                           data=data,
                           length=len(data),
                           count=len(data))
    # Define the collection that data will be pulled from
    all_data = search_db('SELECT * FROM master_skies LIMIT 100')

    # Define properties to show in table
    fields = list(cursor.column_names)

    names = []
    for file in all_data:
        names.append(url_safe(file[0]))

    length = len(all_data)
    return render_template('skies.html',
                           fields=fields,
                           names=names,
                           data=all_data,
                           length=length,
                           count=length)

@app.route('/fitsview')
@login_required
def fitsview():
    '''
    Creates a table of all information on a given file and prepares for image generation.
    '''
    # Generate the appropriate filepath
    url_safe_name = request.args.get('url_safe_name').encode('ascii')
    address = request.args.get('address')
    url_safe_name = url_safe_name.decode('ascii')
    filename =root_dir + url_safe_name.replace('-', '/')

    hdu = fits.open(filename)
    fields = hdu[0].header
    items = []
    for key in fields:
        if (key, hdu[0].header[key]) not in items:
            items.append((key, hdu[0].header[key]))

    # Generate appropriate list of files which went into creating given file
    file_list=[]
    if 'flat' in filename or 'dark' in filename or 'sky' in filename:
        flist = filename[:-5] + '_files.list'
        f = open(flist, 'r')
        file_list = [line.rstrip('\n') for line in f]
        f.close()
    elif 'cal' in filename:
        file_list.append(fields['RAW_FN'])
        file_list.append(fields['DARK_FN'])
        file_list.append(fields['FLAT_FN'])
        try:
            if fields['SKY_FN'] != 'None':
                file_list.append(fields['SKY_FN'])
        except KeyError:
            pass
    hdu.close()

    return render_template('fitsview.html',
                            items=items,
                            filename=filename, address=address, file_list=file_list,
                            url_safe=url_safe)
# @app.route('/search/target/<url_safe_name>')
# def target2(url_safe_name):
#     pattern = url_safe_name.replace('_', '.*')
#     target = db.targets.find_one({'Name': {'$regex':pattern}}, {'_id': 0})
#     items = []
#     for key, value in target.items():
#         items.append((key, value))
#     fc_vars = db.targets.find_one({'Name':{'$regex':pattern}}, {'_id':0,
#                                   'Name': 1, 'RA':1, 'DEC':1})
#     var_list = []
#     for var in fc_vars.items():
#         var_list.append(var[1])
#     name, ra, dec = var_list
#     name = name.replace(' ', '_')
#     maskDraw.findingChart(ra, dec, 'J',  14.5,
#                             target_name = name,
#                             output_prefix='app/static/img/'+name+'_')
#     fname = '../static/img/'+name+'_'+'finding_chart_'+ str(ra)+'_'+str(dec)+'J'+'.png'
#     return render_template('object.html',
#                             items=items,
#                             fname=fname,
#                             name=name)

@app.route('/search/a', methods=['GET', 'POST'])
def append():
    '''
    Add a parameter to the query
    '''
    global form
    global num
    if len(form.queries) < form.queries.max_entries and request.method == 'GET':
        form.queries.append_entry()
        num += 1
    hostname = socket.gethostname()
    if hostname == 'riri':
        return redirect('http://riri.caltech.edu/search')
    else:
        return redirect('/search')

@app.route('/search/p', methods=['GET', 'POST'])
def pop():
    '''
    Return to one search parameter
    '''
    global form
    global num
    while len(form.queries) > 1 and request.method == 'GET':
        form.queries.pop_entry()
        num -= 1
    hostname = socket.gethostname()
    if hostname == 'riri':
        return redirect('http://riri.caltech.edu/search')
    else:
        return redirect('/search')

@app.route('/search', methods =['GET', 'POST'])
@login_required
def search():
    '''
    This function governs the search page
    '''
    global form
    global num
    # If the user has entered values and submitted
    if request.method == 'POST':
        # Build the query based on values entered
        query = build_search_query(num)
        fields = []
        names = []
        # Gather information fromd database
        data = search_db(query)
        for field in cursor.description:
            fields.append(field[0])
        # Move Name to the front for finding chart and info links
        if(u'Name' in fields):
            name_ind = fields.index(u'Name')
            fields.remove(u'Name')
            fields.insert(0, u'Name')
            for i in range(0, len(data)):
                temp = data[i][name_ind]
                data[i] = [temp] + data[i][:name_ind] + data[i][name_ind + 1:]
                names.append(url_safe(data[i][0]))
        return render_template('search_result.html',
                       fields=fields,
                       names=names,
                       data=data,
                       length=len(data),
                       count = len(data))
    else:
        return render_template('search.html',
                                  form=form)

@app.route('/fc', methods = ['GET', 'POST'])
@login_required
def finding_chart():
    '''
    Use Kaew's finding chart program to create a finding chart for a given target
    '''
    form = FindingForm()
    if request.method == 'POST':
        name = request.form['name']
        ra = float(request.form['RA'])
        dec = float(request.form['Dec'])
        maskDraw.findingChart(ra, dec, 'J',  14.5,
                            target_name = name,
                            output_prefix='app/static/img/'+name+'_')
        fname = '../static/img/'+name.replace(' ', '_')+'_'+'finding_chart_'+ str(ra)+'_'+str(dec)+'J'+'.png'
        return render_template('fc.html',
                               fname = fname)
    else:
        return render_template('create_fc.html',
                               form=form)

@app.route('/plot_query', methods = ['GET', 'POST'])
@login_required
def plot_query():
    '''
    Generate a webpage which will allow the user to query the database for no more than two
    numerical variables and plot them against each other.
    '''
    # If the user has submitted a query
    if request.method == 'POST':
        # query = format_query(request.form['query'])
        query = request.form['query']
        error = None
        if not query:
            error = 'Please enter a query!'
        if error is not None:
            flash(error)
        else:
            # Gather data from the database
            data_raw = search_db(query)
            data = []
            for i in range(len(data_raw)):
                if data_raw[i][0] != None and data_raw[i][1] != None:
                    data.append(data_raw[i])
            # Error checking
            if len(cursor.column_names) != 2:
                flash('Please query for exactly 2 parameters.')
            elif not (str.isdigit(str(data[0][0]).encode('ascii').replace('.', '').replace('-', '')) and str.isdigit(str(data[0][1]).encode('ascii').replace('.', '').replace('-', ''))):
                flash('Please query only for numeric parameters.')
            else:
                # Format the data appropriately to be used in generating the plot and displaying it
                x_label = cursor.column_names[0]
                y_label = cursor.column_names[1]
                coords = []
                for row in data:
                    if row[0] != None and row[1] != None and str.isdigit(str(row[0]).encode('ascii').replace('.', '').replace('-', '')) and str.isdigit(str(row[1]).encode('ascii').replace('.', '').replace('-', '')):
                        coords.append((row[0], row[1]))
                coords.sort()
                fname = '../static/plots/'+query.upper().replace(' ', '').replace(',', '.').replace('`', '') +'.png'
                file = Path('app' + fname[2:])

                var1 = '_'.join([str(x[0]) for x in coords])
                var2 = '_'.join([str(y[1]) for y in coords])
                # Generate the webpage with non-empty values which will be used in plot generation
                return render_template('plot_query.html',
                               var1=var1, var2=var2, x_label=x_label, y_label=y_label, data=coords, fields=cursor.column_names, length=len(coords))
    # Empty values indicate no plot is being generated
    return render_template('plot_query.html', x_label='', y_label='', var1='', var2='', data=[], fields=[])

@app.route('/create_plot')
def create_plot():
    '''
    This function handles the process of creating a plot based on numerical queries
    as fielded by the webpage /plot_query. It will save the plot to memory, then
    display it on the webpage (does not save anything to disk).
    '''
    # Retrieve the numerical coordinate values (String arguments were required)
    var1 = [float(x) for x in request.args.get('var1').split('_')]
    var2 = [float(x) for x in request.args.get('var2').split('_')]
    plt.clf()
    img = BytesIO()
    # Plot the values
    plt.plot(var1, var2, 'ob')
    plt.xlabel(request.args.get('x_label'))
    plt.ylabel(request.args.get('y_label'))
    #plt.savefig('app' + fname[2:])
    # Save the plot to a Bytes object in memory and
    plt.savefig(img, format='png')
    img.seek(0)
    # This will send the appropriate image data to be displayed
    return send_file(img, mimetype='image/png')

@app.route('/create_fits')
def create_fits():
    '''
    This function, similarly to create_plot() is responsible for creating a
    pyplot of a fits image and storing it to memory to be displayed on /fitsview
    '''
    plt.clf()
    img = BytesIO()
    # Get the filename
    fname = request.args.get('filename')
    hdu = fits.open(fname)
    # Plot the information, adjusting to improve contrast
    vmin = np.percentile(hdu[0].data, 1)
    vmax = np.percentile(hdu[0].data, 99)
    plt.imshow(hdu[0].data, origin='lower', vmin=vmin, vmax=vmax)
    plt.colorbar()
    # Save the figure to memory (BytesIO object)
    plt.savefig(img, format='png')
    img.seek(0)
    hdu.close()
    # Send the image data to the fitsview page
    return send_file(img, mimetype='image/png')

@app.route('/guide')
@login_required
def guide():
    '''
    Display the page with the website user guide. Includes informations such as
    SQL tutorials and query formatting
    '''
    return render_template('guide.html')
