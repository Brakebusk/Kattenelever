#!/usr/bin/env python3

#Creates a new user with the given parameters

import cgi
import pymysql
from argon2 import PasswordHasher

def escape(s): #Simple html escape for when displaying information and shit
	return s.replace("<", "&lt;").replace(">", "&gt;")

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')

username = escape(formdata.getvalue('username'))
password = formdata.getvalue('password')
email = escape("" + str(formdata.getvalue("email")))
usertype = escape(formdata.getvalue('usertype'))
access = escape(formdata.getvalue('access'))

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

cursor = connection.cursor()
sql = "SELECT userid FROM usertable WHERE role='Administrator' AND session=%s"
cursor.execute(sql, (session))
response = cursor.fetchone()
cursor.close()

if response: #user is an Admin
	ph = PasswordHasher()
	passhash = ph.hash(password)
	
	if usertype == "Administrator":
		access = "All"
	
	cursor = connection.cursor()
	sql = "INSERT INTO usertable (username, passhash, role, groupname, email) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(sql, (username, passhash, usertype, access, email))
	cursor.close()
	
	connection.commit()
		
	print("Content-type: text/html; charset=UTF-8")
	print()

connection.close()