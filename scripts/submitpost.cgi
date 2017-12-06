#!/usr/bin/env python3

#Creates a new post. XSS is possible lol.

import cgi
import pymysql
from datetime import datetime

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
title = formdata.getvalue('title').replace("<script>", "").replace("</script>", "")
content = formdata.getvalue('content').replace("<script>", "").replace("</script>", "")
group = formdata.getvalue('group')
postType = formdata.getvalue("type")
startpoint = formdata.getvalue("startpoint")
endpoint = formdata.getvalue("endpoint")
location = formdata.getvalue("location")

if postType != "event":
	startpoint = ""
	endpoint = ""
	location = ""

print("Content-type: text/html; charset=UTF-8")
print()

try:
	connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
	
	cursor = connection.cursor()
	sql = "SELECT groupname, username FROM usertable WHERE session=%s"
	cursor.execute(sql, (session))
	response = cursor.fetchone()
	cursor.close()
	
	if group == response[0] or response[0] == "All":
		cursor = connection.cursor()
		sql = "INSERT INTO posts (title, content, creationtime, author, groupname, type, startpoint, endpoint, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(sql, (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), response[1], group, postType, startpoint, endpoint, location))
		cursor.close()
		connection.commit()
		print("{SUCCESS}")
	else:
		print("{FAILURE} Restricted access")

	connection.close()
except:
	print("{FAILURE}")