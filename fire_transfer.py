#! /usr/bin/env python

import sys
import os
import datetime
import time
import paramiko
import mysql.connector as mariadb
import string
import itertools

# paramiko logs
paramiko.util.log_to_file("/var/log/paramiko.log")

# Time for the email messages
date = datetime.datetime.today();
year = date.year
month = date.month
day = date.day
hour = date.hour
minute = date.minute

# SFTP Private Key
keyfile = paramiko.RSAKey.from_private_key_file("/root/.ssh/example.pem");
username = 'example'

# Open a transport
host,port = "example.example.com",22
transport = paramiko.Transport((host,port))

# Paths
local_path = '/mnt/fire/'
remote_path = '/memphisTN/'

# Open database connection
mariadb_connection = mariadb.connect(user='example', password='ThisIsBadIknow', database='example')
cursor = mariadb_connection.cursor()

# Queries
transfer_completed_query = "SELECT file_name FROM transactions WHERE transfer_completed = 'no';"
transfer_completed_update = "UPDATE transactions SET transfer_completed = 'yes' WHERE file_name = %s"
copy_completed_update = "UPDATE transactions SET alastar_copied = 'yes' WHERE file_name = %s"
cursor.execute(transfer_completed_query);
result = cursor.fetchall();

# Lists, transfer_List is files that need to be transmitted, transmit_list is files that have been transferred.
result_List = list(result);
transfer_List = [];
copied_List = [];
transmit_list = [];

# Converts unicode tuple in result_List to string in transfer_List
tuple = result_List
out = list(itertools.chain(*tuple))
for i in out:
	transfer_List.append(i)

#attempt = iter(range(0, 30))

def transmit():
	"Performs the SFTP Put, Records the put in the database, copies the file to applications folder"
	sftp.put(source, destination)
	print("Transmitted " + i)
	transmit_list.append(i)
	cursor.execute(transfer_completed_update, j)
	mariadb_connection.commit()

def copy():
	"Copies the files to the applications team for Alastar processing"
	os.system("cp /mnt/fire/" + i + " /mnt/ati/" + i)
	copied_List.append(i)
	cursor.execute(copy_completed_update, j)
	mariadb_connection.commit()

# Incremented to control the number of files transferred in a given run (there have been thousands lately and this needs to be limited 05/28/2020)
if len(transfer_List) >= 1:

	# Opens SFTP Connection
	transport.connect(None,username, pkey = keyfile)
	sftp = paramiko.SFTPClient.from_transport(transport)

	# Transmit Files
	for i, j in map(None, transfer_List, result_List):

		# These represent the string list and the tuple list
		file_name = i
		file_name2 = j

		# Source and Destination directories
		source = str(local_path + str(file_name))
		destination = str(remote_path + str(file_name))

		# Uses the tuple list to update the database on which files have been transferred
		if os.path.exists(local_path + i) == True:
			try:
				transmit()

			except mariadb.Error as err:
				print("Error: {}".format(err))
			except IOError, ioerr:
				print("I/O error({0}): {1}".format(ioerr.errno, ioerr.strerror))
				print(i + ": Transmit Errored out")
				os.system("mv /mnt/fire/" + i + " /storage/fire/errors/" + i)
				print("Moved error file " + i + " to /storage/fire/errors/")
				pass
			except paramiko.ssh_exception as para_ssh:
				print("Transport SSH Error on this File")
			except: # Catch all errors
				e2 = sys.exc_info()[0]
				print("Generic Error: " + str(e2))

	#Close sftp, transport, and database connections.
	sftp.close()
	transport.close()
	mariadb_connection.close()

# Reads variables from /scripts/fire/variable_file.txt to keep track of numbers for email notifications
variables = {}

with open("/scripts/fire/variable_file.txt") as file:
        for line in file:
                name, value = line.split("=")
                variables[name] = int(value)

sent1 = variables["sent_files"]
copied1 = variables["copied_files"]
print("Sent value from file = " + str(sent1)) #printed for logs
print("Copied value from file = " + str(copied1)) #printed for logs

# Updates variables in /scripts/fire/variable_file.txt
sent2 = sent1 + len(transmit_list)
copied2 = copied1 + len(copied_List)
print("Sent = " + str(sent2)) #printed for logs
print("Copied = " + str(copied2)) #printed for logs

if len(transfer_List) >= 1:
        try:
               	os.system("echo > variable_file.txt")
		data = """sent_files={sent}\ncopied_files={copied}\n""".format(sent=str(sent2), copied=str(copied2))
		variable_file = open("/scripts/fire/variable_file.txt", "rw+")
               	variable_file.writelines(data)
                variable_file.close()
        except:
                print("Unexpected error:", sys.exc_info()[0])
