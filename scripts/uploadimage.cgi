#!/usr/bin/env python3

#Takes image information and stores it on the server

import cgi
import pymysql
import base64
import os
import string
import random

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
datastring = formdata.getvalue('datastring')

print("Content-type: text/html; charset=UTF-8")
print()

def randomValueGenerator(size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

try:
	scriptpath = os.path.dirname(os.path.realpath(__file__))
	if os.name == "nt": #if windows
		dirPath = scriptpath.replace("scripts", "") + "media\\postimages\\"
	else:
		dirPath = scriptpath.replace("scripts", "") + "media/postimages/"
	
	imageformat = datastring.split(",")[0].split("/")[1].split(";")[0]
	base64data = datastring.split(",")[1]
	imagename = randomValueGenerator(32) + "." + imageformat
	imagepath  = dirPath + imagename
	
	with open(imagepath, "wb") as fh:
		fh.write(base64.decodestring(base64data.encode('utf-8')))
	
	print("{SUCCESS}§" + imagename)
except:
	print("Error")