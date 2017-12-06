#!/usr/bin/env python3

#Edits the selected post

import cgi
import pymysql
from datetime import datetime

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
title = formdata.getvalue('title').replace("<script>", "").replace("</script>", "")
content = formdata.getvalue('content').replace("<script>", "").replace("</script>", "")
postid = formdata.getvalue('postid')

print("Content-type: text/html; charset=UTF-8")
print()

try:
	connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
	
	cursor = connection.cursor()
	sql = "SELECT groupname, username FROM usertable WHERE session=%s"
	cursor.execute(sql, (session))
	response = cursor.fetchone()
	cursor.close()
	
	cursor = connection.cursor()
	sql = "SELECT groupname FROM posts WHERE postid=%s"
	cursor.execute(sql, (postid))
	group = cursor.fetchone()[0]
	cursor.close()
	
	if group == response[0] or response[0] == "All":
		cursor = connection.cursor()
		sql = "UPDATE posts SET title=%s, content=%s, edittime=%s WHERE postid=%s"
		cursor.execute(sql, (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), postid))
		cursor.close()
		connection.commit()
		print("{SUCCESS}")
	else:
		print("{FAILURE} Restricted access")

	connection.close()
except:
	print("{FAILURE}")