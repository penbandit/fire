# Fire

Transfers files via SFTP from working directory to Example

Copies files to a separate working directory for Example project (This is a handoff point to applications team).

Keeps a database of what files have been transferred and copied respectively.

cron.lock (flock utility) files are to prevent race conditions in cron scheduled jobs.

db_update.py runs every minute. Identifies files in the directory that are not already in the database and records them to be trasnferred by fire_transfer.py

fire_transfer.py checks the database every minute for files that have not been transferred, opens an SFTP connection and transfers the files, updating the database record to indicate the transfer is completed for that file.

