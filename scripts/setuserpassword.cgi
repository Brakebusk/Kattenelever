#!/usr/bin/env python3

#Sets a new password for the selected userid (session user must be an administrator)

import cgi
import pymysql
from argon2 import PasswordHasher

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')

userid = formdata.getvalue('userid')
new_pass = formdata.getvalue('newpass')

print("Content-type: text/html; charset=UTF-8")
print()

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

cursor = connection.cursor()
sql = "SELECT userid FROM usertable WHERE role='Administrator' AND session=%s"
cursor.execute(sql, (session))
response = cursor.fetchone()
cursor.close()

if response:
	ph = PasswordHasher()
	new_hash = ph.hash(new_pass)
	cursor = connection.cursor()
	sql = "UPDATE usertable SET passhash=%s WHERE userid=%s"
	cursor.execute(sql, (new_hash, userid))
	cursor.close()
	connection.commit()
	print("{SUCCESS}")
else:
	print("Ingen tilgang")

connection.close()
	