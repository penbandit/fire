#! /usr/bin/env python

import os
import system

list_Contents = os.listdir("/mnt/fire/")
target_File = []

# Source and Target Directories
source_Directory = "/mnt/fire/"
target_Directory = "/storage/fire/fire_archive.zip"

def archive():
    "Zips the file into the target directory archive and removes the original"
    os.system("zip " + target_Directory + " " + source_Directory + i)
    os.remove(source_Directory + i)

for i in list_Contents:
    if i.lower().endswith(('.xml')):
        target_File.append(i)

if len(target_File) >= 1:
    for i in target_File:
        if os.path.exists(source_Directory + i) == True:
            archive()