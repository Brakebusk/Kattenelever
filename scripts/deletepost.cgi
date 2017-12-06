#!/usr/bin/env python3

#Deletes selected post if the user has proper authority to do so

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
postid = formdata.getvalue('postid')

print("Content-type: text/html; charset=UTF-8")
print()

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
cursor = connection.cursor()
sql = "SELECT groupname FROM usertable WHERE session=%s"
cursor.execute(sql, (session))
userGroupname = cursor.fetchone()
cursor.close()

if userGroupname:
	cursor = connection.cursor()
	sql = "SELECT groupname FROM posts WHERE postid=%s"
	cursor.execute(sql, (postid))
	postGroupname = cursor.fetchone()
	cursor.close()
	
	if postGroupname:
		if userGroupname[0] == postGroupname[0] or userGroupname[0] == "All": #user has permission to delete post
			cursor = connection.cursor()
			sql = "DELETE FROM posts WHERE postid=%s"
			cursor.execute(sql, (postid))
			cursor.close()
			connection.commit()
			print("{SUCCESS}")
		else:
			print("{ERROR}")
	else:
		print("{ERROR}")
else:
	print("{ERROR}")