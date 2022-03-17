#! /usr/bin/env python

import os
import datetime
import time

# Time for the email messages
date = datetime.datetime.today();
year = date.year
month = date.month
day = date.day
hour = date.hour
minute = date.minute

# Reads variables from /scripts/fire/variable_file.txt to keep track of numbers for email notifications
variables = {}

with open("/scripts/fire/variable_file.txt") as file:
        for line in file:
                name, value = line.split("=")
                variables[name] = int(value)

sent = variables["sent_files"]
copied = variables["copied_files"]

# Formats the email message.
file_Count = sent
copy_Count = copied
email = open("/scripts/fire/fire_transfer_email_template.txt", "w+")
body = """XML FILES TRANSFERRED TODAY:
Date: {month}-{day}-{year}
Time: {hours}:{minute}
XML Files Transferred Today: ({file_Count})

This is an automated notification, please verify the files transferred to ensure accuracy.

Thank you,
City IS""".format(month=str(month), day=str(day), year=str(year), hours=str(hour), minute=str(minute), file_Count=str(file_Count), copy_Count=str(copy_Count))
email.writelines(body)
email.close()

# Warning email if the count seems low
warning_email = open("/scripts/fire/fire_transfer_warning_email_template.txt", "w+")
warning_email_body = """XML FILES TRANSFERRED TODAY:
Date: {month}-{day}-{year}
Time: {hours}:{minute}
XML Files Transferred Today: ({file_Count})

The count of transferred files is below the tresh hold of (1000).
This indicates that there may be a problem with the transfer process.
Thank you,
City IS""".format(month=str(month), day=str(day), year=str(year), hours=str(hour), minute=str(minute), file_Count=str(file_Count), copy_Count=str(copy_Count))
warning_email.writelines(warning_email_body)
warning_email.close()

# Send the email.
if sent <= 1000:
        os.system("cat /scripts/fire/fire_transfer_warning_email_template.txt | mail -s \'Daily Transfer Warning\' example@example.com")
else:
        os.system("cat /scripts/fire/fire_transfer_email_template.txt | mail -s \'Daily Transfer\' example@example.com")

# Reset the variables to 0
counter = """sent_files=0\ncopied_files=0\n"""
if copied >= 1:
        try:
	        os.system("echo > /scripts/fire/variable_file.txt")
                variable_file = open("/scripts/fire/variable_file.txt", "rw+")
                variable_file.writelines(counter)
                variable_file.close()
        except:
                print("Unexpected error:", sys.exc_info()[0])