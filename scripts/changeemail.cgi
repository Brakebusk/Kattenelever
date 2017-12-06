#!/usr/bin/env python3

#This script changes the email of the user

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue("session")
new_email = formdata.getvalue("newemail")

print("Content-type: text/html; charset=UTF-8")
print()

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

def changeemail(userid):
	cursor = connection.cursor()
	sql = "UPDATE usertable SET email=%s WHERE userid=%s"
	cursor.execute(sql, (new_email, userid))
	cursor.close()
	connection.commit()
	print("{SUCCESS}")

try:
	cursor = connection.cursor()
	sql = "SELECT userid FROM usertable WHERE session=%s"
	cursor.execute(sql, (session))
	response = cursor.fetchone()
	cursor.close()
	if response:
		changeemail(response[0])
	connection.close()
		
except:
	print("{FAILURE} Fikk ikke endret e-postadresse. (scriptfeil)")