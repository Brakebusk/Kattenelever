#!/usr/bin/env python3

#Checks if visitor is logged in to an account with a valid session token

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')

print("Content-type: text/html; charset=UTF-8")
print()

try:
	connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
	sql = "SELECT username, groupname FROM usertable WHERE session=%s"
	cursor = connection.cursor()
	cursor.execute(sql, session)
	response = cursor.fetchone()
	if response:
		print("{LOGGEDIN}")
		print("<username>" + response[1] + "</username>")
		print("<access>" + response[0] + "</access>")
	else:
		print("Invalid session token")
	cursor.close()
	connection.close()
except:
	print("Error")