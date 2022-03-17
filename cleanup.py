#! /usr/bin/env python

import sys
import os
import datetime
import time
import mysql.connector as mariadb
import string
import itertools

# Today's Date
date = datetime.datetime.today();
month = date.month
day = date.day
year = date.year
today = str(str(month) + "/" + str(day) + "/" + str(year))

# Open database connection
mariadb_connection = mariadb.connect(user='example', password='ThisIsBadIKnow', database='example')
cursor = mariadb_connection.cursor()

# Execute Query
#select_query = """SELECT file_name FROM transactions WHERE transfer_completed = 'yes' AND transaction_date = %s"""
select_query = """SELECT file_name FROM transactions WHERE transfer_completed = 'yes' and archived = 'yes'"""
cursor.execute(select_query)
result = cursor.fetchall()
mariadb_connection.close()

# Lists
result_List = list(result);
copied_List = [];

# Converts unicode tuple in result_List to string in copied_List
tuple = result_List
out = list(itertools.chain(*tuple))
for i in out:
	copied_List.append(i)

# Source and Target Directories
source_Directory = "/mnt/fire/"
target_Directory = "/storage/fire/fire_archive.zip"

def archive():
    "Zips the file into the target directory archive and removes the original"
    #os.system("zip " + target_Directory + " " + source_Directory + i)
    os.remove(source_Directory + i)
    #print("zipped " + target_Directory + " " + source_Directory + i)
    print("Deleted:  " + source_Directory + i)

if len(copied_List) >= 1:
    for i in copied_List:
        if os.path.exists(source_Directory + i) == True:
            archive()
