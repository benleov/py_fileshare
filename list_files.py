#!/usr/bin/python

###################### Unique File URL Generator - list files ######################
##
## This script generates unique HTTP URL's for every file in a given directory. 
## It provides a fairly secure way of providing anonymous file access to third party
## without having to supply a username and password or any other form of 
## authentication.
##
## The links are in the format: http://server/files/index.py?file=12386123978624914 
##
## Source: http://programminglinuxblog.blogspot.com/
##
## License: GPLv3. See http://www.gnu.org/licenses/gpl.html
##
####################################################################################

import os
import sys
from mod_python import apache

from mod_python import util

import hashlib

ROOT_FILE_DIR = "/var/www/files" # the directory our files are located

# lists all files in directory and its associated hash value

def index( ):

	webpage = ""
	webpage += "<html><head><title>File Repository</title></head><body>"   # HTML
	webpage += "<h2>File Listing</h2>"
	webpage += "<table><tr><td>FileName</td><td>URL</td></tr>"
	allHashs = getMDDirectoryList()

	for fileName in allHashs.keys():
		url = "http://your_server_ip/files/index.py?file=" + fileName
		webpage += "<tr><td>" + allHashs.get(fileName) + "</td>" + "<td><a href='" + url +  "'>Download Link</a></td></tr>"  

	webpage +="</table></html>"

	return webpage

def getMDDirectoryList():
	filelist = os.walk(ROOT_FILE_DIR)

	md5list = {}

	# recurse through all directories
	# calculate root dir name size so only realtive dirs are shown

	rootFileNameLen = len(ROOT_FILE_DIR) + 1

	for root, dirs, files in filelist:
		for name in files:
			fullPath = os.path.join(root,name)
			md5val = getMDString(fullPath)
			md5list[md5val] = fullPath[rootFileNameLen:len(fullPath)]

	return md5list

# returns the MD of a particular file
def getMDString(filename):
	fileObj = file(filename)
	h = hashlib.new('ripemd160')
	h.update(fileObj.read());
	return h.hexdigest()

index()


