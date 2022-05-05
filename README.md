# Fire

Transfers files via SFTP from working directory to Example

Copies files to a separate working directory for Example project (This is a handoff point to applications team).

Keeps a database of what files have been transferred and copied respectively.

cron.lock (flock utility) files are to prevent race conditions in cron scheduled jobs.

db_update.py runs every minute. Identifies files in the directory that are not already in the database and records them to be trasnferred by fire_transfer.py

fire_transfer.py checks the database every minute for files that have not been transferred, opens an SFTP connection and transfers the files, updating the database record to indicate the transfer is completed for that file.  Writes the number of transferred files into a text file for use with email_notification.py

email_notification.py reads the data from the text file and sends a notification to the MFD IT Chief of how many files were transferred the previous day.  There's a condition in the script that sends a warning message if the amount of transferred files is below average, indicating that there may be a problem with the transfer automation.

cleanup.py and 
