#!/usr/bin/env python3

#Deletes selected user (given proper authority to do so of course)

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
userid = formdata.getvalue('userid')

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

cursor = connection.cursor()
sql = "SELECT userid FROM usertable WHERE role='Administrator' AND session=%s"
cursor.execute(sql, (session))
response = cursor.fetchone()
cursor.close()

if response: #user is an Admin
	cursor = connection.cursor()
	sql = "DELETE FROM usertable WHERE userid=%s"
	cursor.execute(sql, (userid))
	cursor.close()
	
	connection.commit()
		
	print("Content-type: text/html; charset=UTF-8")
	print()

connection.close()