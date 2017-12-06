#!/usr/bin/env python3

#Edits side panel information for selected section

import cgi
import pymysql
import base64
import os

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
section = formdata.getvalue('section')
title = formdata.getvalue('title').replace("<script>", "").replace("</script>", "")
content = formdata.getvalue('content').replace("<script>", "").replace("</script>", "")
if content == 'none':
	content = ""
image = formdata.getvalue('image')

print("Content-type: text/html; charset=UTF-8")
print()

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

def updateImage():
	scriptpath = os.path.dirname(os.path.realpath(__file__)) #scriptpath = X:\[...]\http-filedirectory\scripts
	
	cursor = connection.cursor()
	sql = "SELECT groupimage FROM groups WHERE groupname=%s"
	cursor.execute(sql, (section))
	oldImageName = cursor.fetchone()[0]
	cursor.close()
	
	if oldImageName is not None: #if there is already an image there, delete it
		if os.name == "nt": #if windows
			oldImagePath = scriptpath.replace("scripts", "") + "media\\titleimages\\" + oldImageName #= X:\[...]\media\titleimages\sos.png
		else:
			oldImagePath = scriptpath.replace("scripts", "") + "media/titleimages/" + oldImageName #= X:\[...]\media\titleimages\sos.png
			
		try:
			os.remove(oldImagePath)
		except:
			whathappened = "¯\_(ツ)_/¯"
	
	imageformat = image.split(",")[0].split("/")[1].split(";")[0]
	base64data = image.split(",")[1]
	imagefilename = section.replace("å", "a") + "." + imageformat
	if os.name == "nt":
		imagepath = scriptpath.replace("scripts", "") + "media\\titleimages\\" + imagefilename
	else:
		imagepath = scriptpath.replace("scripts", "") + "media/titleimages/" + imagefilename
		
	with open(imagepath, "wb") as fh:
		fh.write(base64.decodestring(base64data.encode('utf-8')))
	
	cursor = connection.cursor()
	sql = "UPDATE groups SET groupimage=%s WHERE groupname=%s"
	cursor.execute(sql, (imagefilename, section))
	cursor.close()
	

try:	
	cursor = connection.cursor()
	sql = "SELECT groupname, username FROM usertable WHERE session=%s"
	cursor.execute(sql, (session))
	response = cursor.fetchone()
	cursor.close()
	
	if section == response[0] or response[0] == "All":
		cursor = connection.cursor()
		sql = "UPDATE groups SET sidepaneltitle=%s,description=%s WHERE groupname=%s"
		cursor.execute(sql, (title, content, section))
		cursor.close()
		if image != 'none':
			updateImage()
		connection.commit()
		print("{SUCCESS}")
	else:
		print("{FAILURE} Restricted access")

	connection.close()
except Exception as e:
	print("{FAILURE} " + str(e))