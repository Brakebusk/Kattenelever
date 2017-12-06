#!/usr/bin/env python3

#Changes password of user if given current password is correct

import cgi
import pymysql
from argon2 import PasswordHasher

formdata = cgi.FieldStorage()
session = formdata.getvalue("session")
old_pass = formdata.getvalue("old_pass")
new_pass = formdata.getvalue("new_pass")

print("Content-type: text/html; charset=UTF-8")
print()

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

def changepassword(server_passhash):
	old_pass_valid = False
	ph = PasswordHasher()		
	try:
		if ph.verify(server_passhash, old_pass):
			old_pass_valid = True
	except:
		old_pass_valid = False
	if old_pass_valid:
		new_hash = ph.hash(new_pass)
		cursor = connection.cursor()
		sql = "UPDATE usertable SET passhash=%s WHERE session=%s"
		cursor.execute(sql, (new_hash, session))
		cursor.close()
		connection.commit()
		print("{SUCCESS}")
	else:
		print("{FAILURE} Fikk ikke endret passord.")

try:
	cursor = connection.cursor()
	sql = "SELECT passhash FROM usertable WHERE session=%s"
	cursor.execute(sql, (session))
	response = cursor.fetchone()
	cursor.close()
	if response:
		changepassword(response[0])
	connection.close()
		
except:
	print("{FAILURE} Fikk ikke endret passord. (scriptfeil)")