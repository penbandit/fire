#! /usr/bin/env python

import os
import datetime
import time
import mysql.connector as mariadb

#Time stamp creation
date = datetime.datetime.today();
year = date.year
month = date.month
day = date.day
hour = date.hour
minute = date.minute
transaction_date = str(str(month) + "-" + str(day) + "-" + str(year))
transaction_time = str(str(hour) + ":" + str(minute))

#Opens connection to NFORS database.
mariadb_connection = mariadb.connect(user='example', password='ThisIsBadIKnow',database='example')
cursor = mariadb_connection.cursor()

#Source directory
list_Contents = os.listdir("/mnt/fire/");
list_ati_Contents = os.listdir("/mnt/ati");

#Runs through the working directory and builds a list of XML files.
xml_File = [];

for i in list_Contents:
	if i.lower().endswith(('.xml')):
		xml_File.append(i);

#Insert XML file names into database.
for i in xml_File:
	file_name = i
	today = str(str(month) + "/" + str(day) + "/" + str(year))
	query = "INSERT IGNORE transactions (file_name, transaction_date) VALUES (%s, %s)"
	try:
		cursor.execute(query,(file_name, today))
	except mariadb.Error as error:
		print("Error: {}".format(error));

#Commit the previous loops queries and close connection
mariadb_connection.commit();
mariadb_connection.close();
