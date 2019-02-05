from mysql import connector as sql
import csv

# Open the connection to the MySQL server and initialize cursor
connection = sql.MySQLConnection()
connection.connect(host='localhost', user='''removed for security''',
		passwd= '''removed for security''', db='WIRC_POL')
cursor = connection.cursor()

# Create the WIRC_POL database
cursor.execute('CREATE DATABASE IF NOT EXISTS WIRC_POL ')
#cursor.execute('USE WIRC_POL')

### Upload targets to database ###
# Gather the columns to be used, formatting them appropriately for MySQL
# Make all types TEXT(1000), can refine later?
f = open('master_BD.csv', 'r')
columns_str = f.readline()
f.close()
columns_str = columns_str[:-1]
columns_list = columns_str.split(',')
for i in range(0, len(columns_list)):
	columns_list[i] = '`' + columns_list[i] + '`'
columns_str = ' TEXT, '.join(columns_list) + ' TEXT'
columns = '(' + columns_str + ')'
 # for i in range(0, len(columns_list)):
 # 	columns_list[i] += ' TEXT'
columns_type = '(id INT(11) NOT NULL AUTO_INCREMENT, ' + columns_str + ', PRIMARY KEY (id))'
# Create a table to hold the data we will load in, using the gathered columns
cursor.execute("CREATE TABLE IF NOT EXISTS targets "+ columns_type)
# Format the VALUES part of the INSERT INTO query: 'VALUES(%s, %s, ... %s)'
values_str = 'VALUES('
for i in range(0, len(columns_list) - 1):
	values_str += '%s, '
values_str += '%s)'
# Load in the data from the csv file
csv_data = csv.reader(file('master_BD.csv'))
i = 0
# for col in columns_list:
# 	cursor.execute('SELECt * FROM targets LIMIT 1')
# 	cursor.fetchall()
# 	if col not in cursor.column_names:
# 		cursor.execute('ALTER TABLE targets ADD ' + col + ' TEXT')
columns = '(' + ', '.join(columns_list) + ')'
for row in csv_data:
	if i == 0:
		i = 1
		continue
	#cursor.execute('DELETE FROM targets WHERE `Name` = \"{}\"'.format(row[0]))
	cursor.execute('INSERT INTO targets ' + columns + ' ' + values_str, row)

### Upload standards to database ###
# Gather the columns to be used, formatting them appropriately for MySQL
# Make all types TEXT(1000), can refine later
f = open('standards.csv', 'r')
columns_str = f.readline()
f.close()
columns_str = columns_str[:-2]
columns_list = columns_str.split(',')
for i in range(0, len(columns_list)):
	columns_list[i] = '`' + columns_list[i] + '`'
columns_str = ', '.join(columns_list)
columns = '(' + columns_str + ')'
for i in range(0, len(columns_list)):
	columns_list[i] += ' TEXT'
columns_type = '(stan_id INT(11) NOT NULL AUTO_INCREMENT, ' + ', '.join(columns_list) + ', PRIMARY KEY (stan_id))'
# Create a table to hold the data we will load in, using the gathered columns
cursor.execute("CREATE TABLE IF NOT EXISTS standards "+ columns_type)
# Format the VALUES part of the INSERT INTO query: 'VALUES(%s, %s, ... %s)'
values_str = 'VALUES('
for i in range(0, len(columns_list) - 1):
	values_str += '%s, '
values_str += '%s)'
# Load in the data from the csv file
csv_data = csv.reader(file('standards.csv'))
i = 0
for row in csv_data:
	if i == 0:
		i = 1
		continue
	cursor.execute('INSERT INTO standards' + columns + ' ' + values_str, row)

### Upload target references to database ###
# # Gather the columns to be used, formatting them appropriately for MySQL
# # Make all types TEXT(1000), can refine later
f = open('target_refs.csv', 'r')
columns_str = f.readline()
f.close()
columns_str = columns_str[:-2]
columns_list = columns_str.split(',')
for i in range(0, len(columns_list)):
	columns_list[i] = '`' + columns_list[i] + '`'
columns_str = ', '.join(columns_list)
columns = '(' + columns_str + ')'
for i in range(0, len(columns_list)):
	columns_list[i] += ' TEXT'
columns_type = '(tar_id INT(11) NOT NULL, ' + \
				', '.join(columns_list) + ')'
# Create a table to hold the data we will load in, using the gathered columns
cursor.execute("CREATE TABLE IF NOT EXISTS target_refs "+ columns_type)
# Format the VALUES part of the INSERT INTO query: 'VALUES(%s, %s, ... %s)'
values_str = 'VALUES('
for i in range(0, len(columns_list) - 1):
	values_str += '%s, '
values_str += '%s)'
# Load in the data from the csv file
csv_data = csv.reader(file('target_refs.csv'))
i = 0
for row in csv_data:
	if i == 0:
		i = 1
		continue
	cursor.execute('INSERT INTO target_refs' + columns + ' ' + values_str, row)

# Close the connection
connection.commit()
cursor.close()
connection.close()


# The below is used to finish up target_refs id matching
'''
After this is set up, you need to do id matching on target_refs.
On mysql, execute:

UPDATE target_refs
SET tar_id = -1;

INSERT INTO targets (id, Name)
VALUES (-1, "None/Unknown");

UPDATE target_refs, targets
SET target_refs.tar_id = targets.id
WHERE targets.Name LIKE CONCAT("%", target_refs.name) OR
target_refs.Name LIKE CONCAT("2 MASS ", targets.`2MASS Name`);

ALTER TABLE target_refs
ADD INDEX ref_id (tar_id);

ALTER TABLE target_refs
ADD FOREIGN KEY (tar_id)
REFERENCES targets(id);
'''
