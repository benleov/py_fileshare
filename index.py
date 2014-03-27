#!/usr/bin/python

###################### Unique File URL Generator ###################################
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
from mod_python import apache

from mod_python import util

import hashlib

ROOT_FILE_DIR = "/var/www/files" # the directory our files are located

def index(req):
	#   req.content_type = "text/plain"
	webpage = ""

	webpage += "<html><head><title>File Repository</title></head><body>"   # HTML output
	form = util.FieldStorage(req,keep_blank_values=1)

	if (form.has_key("file")):  # process file parameter
		reqHash = form["file"]

		# get dictionary of MD hash values for all files in directory

		allHashs = getMDDirectoryList()

		if ( reqHash in allHashs ):
			webpage +="<h2>File Found: " + allHashs.get(reqHash) + "</h2>"
			webpage += "<a href='" + allHashs.get(reqHash) + "'>Download</a>"
		else:
			webpage += "<h2>unknown file requested</h2>" 
	else:
		webpage += "<h2>No file requested</h2>"

	return webpage + "</body></html>"

# returns dictionary of md5 hashs of files in current directory
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
def getMDString( filename ):
	fileObj = file(filename)
	h = hashlib.new('ripemd160')
	h.update(fileObj.read());
	return h.hexdigest()

def cgiFieldStorageToDict( fieldStorage ):
	"""Get a plain dictionary, rather than the '.value' system used by the cgi module."""
	params = {}

	for key in fieldStorage.keys():
		params[ key ] = fieldStorage[ key ].value

	return params


