#!/usr/bin/env python3

#Loads user information used in settings panel. (Currently only retrieves email address, but can be easily modified to retrieve other things)

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue("session")
new_email = formdata.getvalue("newemail")

print("Content-type: text/html; charset=UTF-8")
print()

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

cursor = connection.cursor()
sql = "SELECT email FROM usertable WHERE session=%s"
cursor.execute(sql, (session))
response = cursor.fetchone()
cursor.close()
if response:
	print(response[0])
	
connection.close()